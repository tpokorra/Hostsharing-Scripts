#!/usr/bin/python3

import os
import getpass
import subprocess

description = """
Check Wordpress installations of my Hostsharing users
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

def get_wordpress_installation_in_path(user, domain, path):
    version_file = "wp-includes/version.php"
    cmd = f'if [ -f {path}/{version_file} ]; then cat {path}/{version_file} | grep "wp_version = "; fi'
    cmd = cmd.replace('"', '\\"')
    stream = os.popen(f'sudo -u {user} -s /bin/bash -c "{cmd}"')
    version = stream.read().strip()
    if version:
        return {'user': user, 'domain': domain, 'path': path, 'version': version.split('=')[1].strip(" ;'")}
    return None


def get_wordpress_installations_of_user(user):

    installations = []
    domains = get_domains_of_user(user)

    for domain in (domains or []):
        installation = get_wordpress_installation_in_path(user, domain, f'~/doms/{domain}/htdocs-ssl')
        if installation:
            installations.append(installation)

        subdomains = get_subdomains_of_domain(user, domain)
        for subdomain in (subdomains or []):
            installation = get_wordpress_installation_in_path(user, f'{subdomain}.{domain}', f'~/doms/{domain}/subs-ssl/{subdomain}')
            if installation:
                installations.append(installation)

    return installations


def get_wordpress_installations_of_pac(pac):

    result = []
    installations = get_wordpress_installations_of_user(pac)
    if installations:
        result += installations
    users = get_users_of_pac(pac)
    for user in (users or []):
        installations = get_wordpress_installations_of_user(f"{pac}-{user}")
        if installations:
            result += installations
    return result

pac = get_current_pac()
installations = get_wordpress_installations_of_pac(pac)
for i in installations:
    print(f"{i['user']:<20} {i['domain']:<40} {i['version']:10} {i['path']}")

