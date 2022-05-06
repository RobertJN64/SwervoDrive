import json

with open('rpi.json') as f:
    on_rpi = json.load(f)

if on_rpi:
    raise Exception("FAKE GPIO ENABLED ON RPI")


BCM = 'BCM'
OUT = True
HIGH = True
LOW = False

def setmode(_mode):
    pass

def setup(_pin, _config):
    pass

def output(_pin, _setting):
    pass

def cleanup():
    pass

class PWM:
    def __init__(self, _pin, _cycle_len):
        pass

    def ChangeDutyCycle(self, _cycle_len):
        pass

    def start(self, _cycle_len):
        pass

