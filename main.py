from LogPrint import FilterReqs
import sys
from time import sleep

sleep(10) #GIVE TIME TO STARTUP

sys.stdout = FilterReqs(sys.stdout)
sys.stderr = FilterReqs(sys.stderr)

import RobotFlask
RobotFlask.serveApp()