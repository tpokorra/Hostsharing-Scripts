#!/usr/bin/python3

#########################################################################################################
# prüfe alle Webseiten, die auf /home/doms verlinkt sind
# entweder als root, oder als Paket Admin
# es wird der aktuelle Status und ein Hash des Inhalts gespeichert.
# Später kann man das Skript wieder aufrufen, und Änderungen am Status oder des Inhalts werden gemeldet.
# Parameter: --dryrun false: es werden Status und Hash in einer lokalen Sqlite Datenbank gespeichert.
# Parameter: --dryrun true: es werden keine Änderungen in der Datenbank gespeichert
#
# Timotheus Pokorra, im Juni 2024
#########################################################################################################

import argparse
import hashlib
import os
import re
import requests
import sqlite3
from datetime import datetime
import pytz
import subprocess
import getpass
from pathlib import Path

# check: select * from website w join (SELECT MAX(timestamp) as t2 FROM website w2) WHERE w.timestamp = t2 AND stability <> 'STABLE';

def is_domain_hosted_by_hostsharing( domain ):
    cmd = [ 'dig', '-t', 'A', domain, '+short' ]
    res = subprocess.run( cmd, capture_output=True, encoding='utf8' )

    return res.stdout.startswith( '83.223.' )

def get_pac(username):
    if "-" in username:
        return username.split('-')[0]
    return username

def get_owner_of_symlink(link):
    f = Path(link)
    if not f.is_symlink():
        return None
    cmd = [ 'ls', '-la', link]
    res = subprocess.run( cmd, capture_output=True, encoding='utf8' )
    owner = res.stdout.split(" ")[2]
    return owner

def check_domain (cursor, url, dryrun, now):

    print(url)
    status_code = -1
    string_hash = None
    exception = None
    #print(url)
    try:
        response = requests.get(url, allow_redirects=True)

        status_code = response.status_code
        if response.status_code == 200:
            content = str(response.content)

            # replace for Nextcloud
            content = re.sub('nonce=".*?"', 'nonce=""', content)

            # replace all values
            content = re.sub('".*?"', '""', content)

            hashobj = hashlib.md5()
            hashobj.update(content.encode('utf-8'))
            string_hash = hashobj.hexdigest()

            #print(f"{url} {response.status_code} {string_hash}")

        else:
            #print(f"{url} {response.status_code}")
            None

    except Exception as err:
        #print(f"exception getting {url}: {err}")
        exception = str(err)

    stability = 'NEW'
    result = cursor.execute("SELECT status_code, string_hash FROM website WHERE url = ? ORDER BY timestamp DESC LIMIT 1", (url,))
    row = result.fetchone()
    if row:
        # check if previous status and hash was the same
        if row[0] == status_code and row[1] == string_hash:
            stability = 'STABLE'
        else:
            stability = 'CHANGED'
            if row[0] != status_code:
                print(f"{url} changed from {status_code} to {row[0]}")
            else:
                print(f"{url} has different content now")
                print(row)
                print(url, status_code, string_hash)

    if not dryrun:
        if stability == 'NEW':
            print(f"adding {status_code} {url}")
        data = [url, now, status_code, string_hash, exception, stability]
        cursor.execute("INSERT INTO website VALUES (?,?,?,?,?,?)", data)

def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

now = datetime.now(pytz.timezone('Europe/Berlin'))
con = sqlite3.connect("monitor-websites.db")
cursor = con.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS website(url, timestamp, status_code, string_hash, exception, stability)")

# dryrun: no writing, just checking
parser = argparse.ArgumentParser(description='Check websites and their availability')
parser.add_argument('--dryrun', type=str2bool, required=True, help='do not update the database')
args = parser.parse_args()
dryrun = args.dryrun
for dir in os.walk("/home/doms/"):
    # check directories or symlinks that we have permissions for (eg. as user root)
    for domain in dir[1]:
        if not is_domain_hosted_by_hostsharing(domain):
            continue
        check_domain(cursor, f"https://{domain}", dryrun, now)
        check_domain(cursor, f"http://{domain}", dryrun, now)
        if not dryrun:
            con.commit()
    # check symbolic links
    current_pac = get_pac(getpass.getuser())
    for domain in dir[2]:

        # ignore if different pac
        owner = get_owner_of_symlink(f"/home/doms/{domain}")
        if get_pac(owner) != current_pac:
            continue

        if not is_domain_hosted_by_hostsharing(domain):
            continue
        check_domain(cursor, f"https://{domain}", dryrun, now)
        check_domain(cursor, f"http://{domain}", dryrun, now)
        if not dryrun:
            con.commit()

con.close();

