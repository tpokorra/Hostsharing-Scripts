#!/usr/bin/python3

import os
import getpass

description = """
Check Wordpress installations of my Hostsharing users
"""

def get_installation(pac, user, path, version_file):
    cmd = f'if [ -f "{path}/{version_file}" ]; then echo "{path}"; fi'
    cmd = cmd.replace('"', '\\"')
    stream = os.popen(f'sudo -u {pac}-{user} -s /bin/bash -c "{cmd}"')
    path = stream.read()
    return path.strip()


def get_installations(pac, user):
    version_file = "wp-includes/version.php"
    path = f"/home/pacs/{pac}/users/{user}/doms"
    installations = []
    domains = get_domains(pac, user)
    for domain in (domains or []):
        installation = get_installation(pac, user, f"{path}/{domain}/htdocs-ssl", version_file)
        if installation:
            installations.append((domain, installation))

        subdomains = get_subdomains(pac, user, domain)
        for subdomain in (subdomains or []):
            installation = get_installation(pac, user, f"{path}/{domain}/subs-ssl/{subdomain}", version_file)
            if installation:
                installations.append((f"{subdomain}.{domain}", installation))

    for (domain, instance_path) in installations:
        cmd = f'cat "{instance_path}/{version_file}" | grep "wp_version = "'
        stream = os.popen(f'sudo -u {pac}-{user} {cmd}')
        version = stream.read().strip()
        if version:
            print(f'{pac}-{user}: {domain}: {version} {instance_path}')


def get_subdomains(pac, user, domain):
    path = f"/home/pacs/{pac}/users/{user}/doms/{domain}/subs-ssl"
    stream = os.popen(f'sudo -u {pac}-{user} -s /bin/bash -c "if [ -d {path} ]; then ls -1 {path}; fi"')
    domains = stream.read()
    if domains:
        return domains.split('\n')
    return None

def get_domains(pac, user):
    path = f"/home/pacs/{pac}/users/{user}/doms"
    stream = os.popen(f'sudo -u {pac}-{user} -s /bin/bash -c "if [ -d {path} ]; then ls -1 {path}; fi"')
    domains = stream.read()
    if domains:
        return domains.split('\n')
    return None


def get_users(pac):
    if not os.path.isdir(f'/home/pacs/{pac}/users'):
        print("Bitte als Paket Admin (eg xyz00) aufrufen")
        exit(-1)

    result = []
    for f in os.scandir(f'/home/pacs/{pac}/users'):
        if f.is_dir():
            result.append(f.name)

    return result


# check all users
pac=getpass.getuser()
users = get_users(pac)

for user in users:
    domains = get_installations(pac, user)

