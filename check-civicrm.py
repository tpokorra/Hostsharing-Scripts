#!/usr/bin/python3

import os
import getpass
import subprocess

description = """
Check Drupal and CiviCRM installations of my Hostsharing users
"""

def get_subdomains_of_domain(user, domain):

    path = f"~/doms/{domain}/subs-ssl"
    stream = os.popen(f'sudo -u {user} -s /bin/bash -c "if [ -d {path} ]; then ls -1 {path}; fi"')
    subdomains = stream.read()
    if subdomains:
        return subdomains.split('\n')
    return None


def get_domains_of_user(user):

    result = {}
    cmd = "if [ -d ~/doms ]; then ls ~/doms -1; fi"
    output = subprocess.getoutput(f'sudo -u {user} -s /bin/bash -c "{cmd}"').split('\n')
    for line in output:
        if line:
            result[line] = {'domain': line, 'user': user}
    return result


def get_domains_of_pac(pac):

    result = {}

    result = get_domains_of_user(pac)
    users = get_users_of_pac(pac)
    for user in (users or []):
        result.update(get_domains_of_user(f"{pac}-{user}"))

    return result

def get_current_pac():
    user = getpass.getuser()
    return user.split('-')[0]


def get_users_of_pac(pac):
    if not os.path.isdir(f'/home/pacs/{pac}/users'):
        return None

    result = []
    for f in os.scandir(f'/home/pacs/{pac}/users'):
        if f.is_dir():
            result.append(f.name)

    return result

def get_installation_in_path(user, domain, path):
    civi_settings_file = "sites/default/civicrm.settings.php"
    drupal_version_file = "core/lib/Drupal.php"

    cmd = f'readlink -f {path}'
    cmd = cmd.replace('"', '\\"')
    stream = os.popen(f'sudo -u {user} -s /bin/bash -c "{cmd}"')
    link_target = stream.read().strip()

    if not link_target.endswith('web'):
        return None

    drupal_path = link_target[:-3]
    drupal_version = None
    civicrm_version = None

    cmd = f'if [ -f {drupal_path}/web/{drupal_version_file} ]; then cat {drupal_path}/web/{drupal_version_file} | grep "const VERSION ="; fi'
    cmd = cmd.replace('"', '\\"')
    stream = os.popen(f'sudo -u {user} -s /bin/bash -c "{cmd}"')
    version = stream.read().strip()
    if version:
        drupal_version = version.split('=')[1].strip(" ;'")

    cmd = f'if [ -f {drupal_path}/composer.json ]; then cat {drupal_path}/composer.json | grep -E "civicrm/civicrm-core.: "; fi'
    cmd = cmd.replace('"', '\\"')
    stream = os.popen(f'sudo -u {user} -s /bin/bash -c "{cmd}"')
    version = stream.read().strip()
    if version:
        civicrm_version = version.split(':')[1].strip(' ,"')

    if drupal_version and civicrm_version:
        return {'user': user, 'domain': domain, 'path': drupal_path, 'drupal_version': drupal_version, 'civicrm_version': civicrm_version}

    return None


def get_installations_of_user(user):

    installations = []
    domains = get_domains_of_user(user)

    for domain in (domains or []):
        installation = get_installation_in_path(user, domain, f'~/doms/{domain}/htdocs-ssl')
        if installation:
            installations.append(installation)

        subdomains = get_subdomains_of_domain(user, domain)
        for subdomain in (subdomains or []):
            installation = get_installation_in_path(user, f'{subdomain}.{domain}', f'~/doms/{domain}/subs-ssl/{subdomain}')
            if installation:
                installations.append(installation)

    return installations


def get_installations_of_pac(pac):

    result = []
    installations = get_installations_of_user(pac)
    if installations:
        result += installations
    users = get_users_of_pac(pac)
    for user in (users or []):
        installations = get_installations_of_user(f"{pac}-{user}")
        if installations:
            result += installations
    return result

pac = get_current_pac()
installations = get_installations_of_pac(pac)
for i in installations:
    print(f"{i['user']:<20} https://{i['domain']:<40} Drupal: {i['drupal_version']:10} CiviCRM: {i['civicrm_version']:10} {i['path']}")

