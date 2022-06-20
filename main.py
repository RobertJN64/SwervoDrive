from LogPrint import FilterReqs
import sys
from time import sleep
import json

with open('rpi.json') as f:
    on_rpi = json.load(f)

if on_rpi:
    sleep(10) #GIVE TIME TO STARTUP

sys.stdout = FilterReqs(sys.stdout)
sys.stderr = FilterReqs(sys.stderr)

import RobotFlask
RobotFlask.serveApp()