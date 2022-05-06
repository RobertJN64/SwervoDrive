import time
import os
import json

with open('rpi.json') as f:
    on_rpi = json.load(f)

if on_rpi:
    class ServoSix:
        servo_min = 500
        servo_max = 2500

        def __init__(self, servo_min=500, servo_max=2500):
            self.servo_min = servo_min
            self.servo_max = servo_max
            # start the service
            os.system("sudo /etc/init.d/servoblaster start")

        def set_servo(self, servo, angle):
            if servo < 1 or servo > 6:
                print("Servo 1 to 6")
            elif angle < 0 or angle > 180:
                print("Angle 0 to 180")
            else:
                servorng = self.servo_max - self.servo_min
                scaler = servorng / 180
                pulse = self.servo_min + angle * scaler
                command = "echo {}={}us > /dev/servoblaster".format(servo, pulse)
                os.system(command)

        def move_servo(self, servo, start_angle, end_angle, delay):
            inc = 1
            angle = start_angle
            if start_angle > end_angle:
                inc = -1
            while angle != end_angle:
                angle += inc
                self.set_servo(servo, angle)
                time.sleep(delay)

        @staticmethod
        def cleanup():
            # stop the service
            os.system("sudo /usr/bin/killall servod")
            # disable it so it doesn't start after reboot'
            os.system("sudo update-rc.d servoblaster disable")

else:
    class ServoSix:
        def __init__(self):
            pass

        def set_servo(self, _servo, _angle):
            pass

        def move_servo(self, _servo, _start_angle, _end_angle, _delay):
            pass

        @staticmethod
        def cleanup():
            pass