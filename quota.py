#!/usr/bin/python3

import os
import pathlib
import subprocess
from datetime import datetime

logPath = os.path.join(pathlib.Path.home(), "quota_log")
logPath = os.path.join(logPath, datetime.now().strftime("%Y-%m-%d"))
if not os.path.exists(logPath):
  os.makedirs(logPath)

def logging(filename, bashCmd):
  with open(os.path.join(logPath, filename), "w") as outfile:
    process = subprocess.Popen(bashCmd, stdout=outfile)

logging("quota.log", ["quota", "-gs"])
logging("du-pac-all.log", ["/usr/local/bin/du-pac"])
logging("du-pac-greater10MB.log", [os.path.join(pathlib.Path.home(), "bin", "du-pac-greater10MB")])
logging("pac-du-quota.log", [os.path.join(pathlib.Path.home(), "bin", "pac-du-quota")])


