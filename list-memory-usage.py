#!/home/pacs/xyz00/bin/.venv/bin/python

# see https://thispointer.com/python-get-list-of-all-running-processes-and-sort-by-highest-memory-usage/
import psutil
import argparse

description = """
Show the processes that are using the most of memory.

First call:
   make init

Call like this:
   ./list-memory-usage
   
   filter by user name:
   ./list-memory-usage --user=kanboard

   filter by process name:
   ./list-memory-usage --name=php

   show total:
   ./list-memory-usage --all
"""
parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('-u','--user', help='Filter by this user name',required=False)
parser.add_argument('-n','--name', help='Filter by this process name',required=False)
parser.add_argument('-a','--all', help='Show all processes',required=False,action='store_false')
args = parser.parse_args()

# Iterate over all running process
processes = []
for proc in psutil.process_iter():
    try:
        # Get process name & pid from process object.
        processName = proc.name()
        processID = proc.pid
        userName = proc.username()
        m_resident = proc.memory_info().rss

        if args.user is not None:
            if userName != args.user:
                continue
        elif args.all == True:
            if userName in ['dovenull', 'postfix', 'root']:
                continue
            if not '-' in userName:
                continue
        if args.name is not None:
            if processName != args.name:
                continue
        elif args.all == True:
            if processName in ['imap',]:
                continue

        if args.all is None and m_resident/1000/1000 < 10:
            continue

        processes.append({'processID': processID, 'userName': userName, 'processName': processName, 'm_resident': m_resident})
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass

total_m_resident = 0
total_per_user = {}
for p in sorted(processes, key=lambda x:x['m_resident'], reverse=True):
    total_m_resident += p['m_resident']
    if not p['userName'] in total_per_user:
        total_per_user[p['userName']] = 0
    total_per_user[p['userName']] += p['m_resident']
    print("{0:<6} ::: {1:<25} ::: {2:<40} ::: {3:>10} MB".format(p['processID'], p['userName'], p['processName'], round(p['m_resident']/1000/1000, 1))) 

print()

for u in total_per_user:
    print("{0:<25}: Total {1:>10} MB".format(u, round(total_per_user[u]/1000/1000, 1)))

print()

print("Total Resident Memory Usage: {0:>10} MB".format(round(total_m_resident/1000/1000,1)))
