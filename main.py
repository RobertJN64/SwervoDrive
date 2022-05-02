from LogPrint import FilterReqs
import sys

sys.stdout = FilterReqs(sys.stdout)
sys.stderr = FilterReqs(sys.stderr)

import RobotFlask
RobotFlask.serveApp()