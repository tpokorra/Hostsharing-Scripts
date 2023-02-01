#!/usr/bin/python3

import os
import getpass
import smtplib

description = """
Check quota of my Hostsharing users
"""

def get_users(pac):
    if not os.path.isdir(f'/home/pacs/{pac}/users'):
        print("Bitte als Paket Admin (eg xyz00) aufrufen")
        exit(-1)

    result = []
    for f in os.scandir(f'/home/pacs/{pac}/users'):
        if f.is_dir():
            result.append(f.name)

    return result


def send_mail(sender, recipient, subject, body):
  try:
    smtpObj = smtplib.SMTP('localhost')
    message = f"From: {sender}\nTo: {recipient}\nSubject: {subject}\n\n{body}"
    smtpObj.sendmail(sender, recipient, message)
    print(f"Email '{subject}' sent to {recipient}")
  except SMTPException:
    print("Error: unable to send email")


def check_quota(pac, user):
    checkErrorMessage="There is a problem with the quota"
    cmd = f'quota -s || echo "{checkErrorMessage}"'
    cmd = cmd.replace('"', '\\"')
    stream = os.popen(f'sudo -u {pac}-{user} -s /bin/bash -c "{cmd}"')
    output = stream.read()
    if checkErrorMessage in output:
        #print(output)
        send_mail(f"cronjob@{pac}.hostsharing.net", f"{pac}@localhost", f"Quota Problem bei {pac}-{user}", output)


# check all users
pac=getpass.getuser()
users = get_users(pac)

for user in users:
    check_quota(pac, user)

