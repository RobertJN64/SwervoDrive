from LogPrint import lprint
import threading

def handle_cmd(cmd):
    if cmd == 'kill':
        return False
    if cmd in ['stop']:
        lprint("Stop CMD recieved.")
    if cmd in ['forward', 'backward', 'left', 'right', 'rtforward', 'ltforward', 'rtbackward', 'ltbackward']:
        lprint("Drive CMD received: ", cmd)
    if cmd in ['spinleft', 'spinright']:
        lprint("Turn CMD received: ", cmd)
    else:
        raise Exception("Uknown cmd: " + str(cmd))
    return True

def worker(incoming_cmds, err_list):
    while True:
        while len(incoming_cmds) == 0:
            pass
        cmd = incoming_cmds.pop()
        try:
            if not handle_cmd(cmd):
                break
        except (Exception,) as e:
            lprint('++++ERROR++++\n' + str(e) + '\n----ERROR----')
            err_list.append(e)

def startRobotThread():
    incoming_cmds = []
    err_list = []
    threading.Thread(target=worker, args=[incoming_cmds, err_list]).start()
    return incoming_cmds, err_list