from LogPrint import lprint, print_log
import flask
from werkzeug.serving import make_server
from time import sleep
import threading
from flask import render_template, jsonify, request
import json

from RobotManager import startRobotThread

with open('rpi.json') as f:
    on_rpi = json.load(f)

class Server:
    @staticmethod
    def shutdown():
        pass
s = Server

lprint("Flask init...")
app = flask.Flask(__name__)
lprint("Robot init...")
robot, incoming_cmds, err_list = startRobotThread()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/status')
def status():
    return jsonify(success=True)

@app.route('/prints')
def prints():
    return '\n'.join(print_log)

@app.route('/traceback')
def traceback():
    if len(err_list) > 0:
        return str(err_list.pop(0))
    else:
        return ""

@app.route('/drive_cmd/<cmd>')
def handle_drive_cmd(cmd):
    incoming_cmds.append(cmd)
    return jsonify(success=True)

@app.route('/setspeeddir')
def set_speed_dir():
    speed = int(request.args.get('spd'))
    direction = int(request.args.get('dir'))
    if speed is None or direction is None:
        return jsonify(sucess=False)
    incoming_cmds.append(('setspeeddir', speed, direction))
    return jsonify(sucess=True)

@app.route('/wheelPos')
def wheelpos():
    data = {'fr': robot.swerve_fr.get_info(),
            'fl': robot.swerve_fl.get_info(),
            'br': robot.swerve_br.get_info(),
            'bl': robot.swerve_bl.get_info()}
    return data

#region demo
@app.route('/error')
def error():
    incoming_cmds.append('demo_error')
    return jsonify(success=True)

@app.route('/print')
def handle_print():
    lprint('This is a demo print statement!')
    return jsonify(success=True)

@app.route('/kill')
def kill():
    incoming_cmds.clear()
    incoming_cmds.append('kill')
    t = threading.Thread(target=shutdown)
    t.start()
    return jsonify(success=True)
#endregion

def serveApp():
    global s
    lprint("Serving app!")
    dest = 'localhost'
    if on_rpi:
        dest = '0.0.0.0'
    s = make_server(dest, 80, app, threaded=True) #change this on RPi to 0.0.0.0
    t = threading.Thread(target=s.serve_forever)
    t.start()
    print("Serving on http://localhost")

def shutdown():
    sleep(1)
    s.shutdown()
    sleep(1)
    print("Shutdown")