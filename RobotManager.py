from LogPrint import lprint
from RobotHardware import Robot
import threading
import traceback

speed = 50
dir_map = {
    'forward': 0, 'backward': 180, 'left': 270, 'right': 90,
    'rtforward': 45, 'rtbackward': 135, 'ltforward': 315, 'ltbackward': 225
}

def handle_cmd(robot: Robot, cmd):
    global speed
    if isinstance(cmd, tuple):
        if cmd[0] == 'setspeeddir':
            lprint('Setting speed to:', cmd[1], '\and direction to:', cmd[2])
            robot.set_all_modules_speed_and_angle(cmd[1], cmd[2])
    elif cmd == 'kill':
        robot.stop()
        robot.shutdown()
        return False
    elif cmd in ['stop']:
        lprint("Stop cmd recieved.")
        robot.stop()
    elif cmd in ['forward', 'backward', 'left', 'right', 'rtforward', 'ltforward', 'rtbackward', 'ltbackward']:
        lprint("Drive cmd received: ", cmd)
        robot.set_all_modules_speed_and_angle(speed, dir_map[cmd])
    elif cmd in ['spinleft', 'spinright']:
        lprint("Turn cmd received: ", cmd)
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
    elif cmd in ['speedup', 'speeddown']:
        if cmd == 'speedup':
            speed = min(speed + 10, 100)
        elif cmd == 'speeddown':
            speed = max(speed - 10, 0)
        lprint("New Speed: ", speed)
        robot.update_speed(speed)
    elif cmd in ['config', 'home']:
        lprint("Unregistered cmd: ", cmd)
    elif cmd == 'demo_error':
        raise Exception("Demo Error!")
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
        except (Exception,):
            e = traceback.format_exc()
            lprint('++++ERROR++++\n' + str(e) + '----ERROR----')
            err_list.append(e)

def startRobotThread():
    robot = Robot()
    incoming_cmds = []
    err_list = []
    threading.Thread(target=worker, args=[robot, incoming_cmds, err_list]).start()
    return robot, incoming_cmds, err_list