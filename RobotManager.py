from LogPrint import lprint
from RobotHardware import Robot
import threading

speed = 50
dir_map = {
    'forward': 0, 'backward': 180, 'left': 270, 'right': 90,
    'rtforward': 45, 'rtbackward': 135, 'ltforward': 315, 'ltbackward': 225
}

def handle_cmd(robot: Robot, cmd):
    if cmd == 'kill':
        robot.stop()
        return False
    if cmd in ['stop']:
        lprint("Stop CMD recieved.")
        robot.stop()
    if cmd in ['forward', 'backward', 'left', 'right', 'rtforward', 'ltforward', 'rtbackward', 'ltbackward']:
        lprint("Drive CMD received: ", cmd)
        robot.set_all_modules_speed_and_angle(speed, dir_map[cmd])
    if cmd in ['spinleft', 'spinright']:
        lprint("Turn CMD received: ", cmd)
        if cmd == 'spinleft':
            robot.swerve_br.set_speed_and_angle(speed, 45)
            robot.swerve_bl.set_speed_and_angle(speed, 135)
            robot.swerve_fl.set_speed_and_angle(speed, 225)
            robot.swerve_fr.set_speed_and_angle(speed, 315)
        if cmd == 'spinright':
            robot.swerve_fl.set_speed_and_angle(speed, 45)
            robot.swerve_fr.set_speed_and_angle(speed, 135)
            robot.swerve_br.set_speed_and_angle(speed, 225)
            robot.swerve_bl.set_speed_and_angle(speed, 315)

    else:
        raise Exception("Uknown cmd: " + str(cmd))
    return True

def worker(robot, incoming_cmds, err_list):
    while True:
        while len(incoming_cmds) == 0:
            pass
        cmd = incoming_cmds.pop()
        try:
            if not handle_cmd(robot, cmd):
                break
        except (Exception,) as e:
            lprint('++++ERROR++++\n' + str(e) + '\n----ERROR----')
            err_list.append(e)

def startRobotThread():
    robot = Robot()
    incoming_cmds = []
    err_list = []
    threading.Thread(target=worker, args=[robot, incoming_cmds, err_list]).start()
    return incoming_cmds, err_list