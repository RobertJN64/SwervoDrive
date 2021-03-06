import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
import json
from servosix.servosix import ServoSix
from IMU import start_monitor_thread

ss = ServoSix(servo_min=200, servo_max=1200)
#DONT USE PINS 4, 17, 18, 27, 22, 23, 24, 25

rotation_lock_tolerance = 10

class MotorController:
    def __init__(self, fwdPin: int, revPin: int, spdPin: int):
        self.fwdPin = fwdPin
        self.revPin = revPin
        self.spdPin = spdPin

        GPIO.setup(self.fwdPin, GPIO.OUT)
        GPIO.setup(self.revPin, GPIO.OUT)
        GPIO.setup(self.spdPin, GPIO.OUT)

        GPIO.output(self.fwdPin, GPIO.LOW)
        GPIO.output(self.revPin, GPIO.LOW)

        self.pwm = GPIO.PWM(spdPin,1000) #1000 is freq
        self.pwm.start(0)
        self.last_dir = True

    def stop(self):
        GPIO.output(self.fwdPin, GPIO.LOW)
        GPIO.output(self.revPin, GPIO.LOW)
        self.pwm.ChangeDutyCycle(0)

    def _set_speed(self, speed):
        self.pwm.ChangeDutyCycle(speed)

    def set_speed(self, speed):
        self.set_motor_speed_and_direction(speed, self.last_dir)

    def set_motor_speed_and_direction(self, speed, motor_direction):
        if motor_direction:
            GPIO.output(self.revPin, GPIO.LOW)
            GPIO.output(self.fwdPin, GPIO.HIGH)
        else:
            GPIO.output(self.fwdPin, GPIO.LOW)
            GPIO.output(self.revPin, GPIO.HIGH)
        self._set_speed(speed)
        self.last_dir = motor_direction

class SwerveModule:
    def __init__(self, name: str, io_config: dict, servo_offset: int, inv_motor: bool):
        self.name = name

        self.servoNumber = io_config["servoNumber"]
        self.motorController = MotorController(io_config['fwdPin'], io_config['revPin'], io_config['spdPin'])
        self.servo_offset = servo_offset
        self.inv_motor = inv_motor

        self.current_speed = 0
        self.current_angle = servo_offset
        self.current_motor_direction = not inv_motor

    def stop(self):
        self.current_speed = 0
        self.motorController.stop()

    def set_speed(self, speed):
        self.current_speed = speed
        self.motorController.set_speed(speed)

    def set_speed_and_angle(self, speed, angle):
        if speed == 0:
            self.stop()
            return

        if speed < 0:
            speed = -speed
            angle = angle + 180

        angle = angle - self.servo_offset
        motor_direction = not self.inv_motor
        angle = angle%360 #works on negative nums

        if angle >= 180:
            angle -= 180
            motor_direction = not motor_direction

        if (self.current_angle - self.servo_offset) < rotation_lock_tolerance and angle > 180 - rotation_lock_tolerance:
            angle = 0
            motor_direction = not motor_direction

        if (self.current_angle - self.servo_offset) > 180 - rotation_lock_tolerance and angle < rotation_lock_tolerance:
            angle = 179
            motor_direction = not motor_direction

        ss.set_servo(self.servoNumber, angle)
        self.motorController.set_motor_speed_and_direction(speed, motor_direction)

        self.current_motor_direction = motor_direction

        if self.inv_motor:
            self.current_motor_direction = not self.current_motor_direction



        self.current_angle = angle + self.servo_offset
        self.current_speed = speed

    def get_info(self):
        return self.current_angle, self.current_motor_direction, self.current_speed

    def __repr__(self):
        return self.name

class Robot:
    def __init__(self):
        with open('robot_io.json') as f:
            robot_config = json.load(f)

        self.swerve_fr = SwerveModule('swerve_fr', robot_config['swerve_fr'], servo_offset=0, inv_motor=False)
        self.swerve_fl = SwerveModule('swerve_fl', robot_config['swerve_fl'], servo_offset=0, inv_motor=False)
        self.swerve_br = SwerveModule('swerve_br', robot_config['swerve_br'], servo_offset=180, inv_motor=True)
        self.swerve_bl = SwerveModule('swerve_bl', robot_config['swerve_bl'], servo_offset=180, inv_motor=True)
        self.swerve_modules = [self.swerve_bl, self.swerve_br, self.swerve_fl, self.swerve_fr]
        self.set_all_modules_speed_and_angle(0, 0)


        self.imu_angle = 0
        self.imu_calib = False
        self.field_align = False
        self.reset_imu = False
        self.killlist = [False]
        start_monitor_thread(self)

    def stop(self):
        for smodule in self.swerve_modules:
            smodule.stop()

    def robot_init(self):
        for smodule in self.swerve_modules:
            smodule.set_speed_and_angle(speed=0, angle=0)

    def _get_sorted_modules(self, target_direction):
        unsorted = [(45, self.swerve_fr), (135, self.swerve_br), (225, self.swerve_bl), (315, self.swerve_fl)]
        relative_target_dir = target_direction - self.imu_angle
        sorted_tups = []
        for tup in unsorted:
            offset = abs(relative_target_dir - tup[0])
            if offset > 180:
                offset = 360 - offset
            sorted_tups.append((offset, tup[1]))
        sorted_tups.sort(key=lambda x:x[0])
        sorted_mods = []
        for item in sorted_tups:
            sorted_mods.append(item[1])
        return sorted_mods


    def get_front_modules(self, target_direction):
        return self._get_sorted_modules(target_direction)[:2]

    def get_back_modules(self, target_direction):
        return self._get_sorted_modules(target_direction)[2:]

    def set_all_modules_speed_and_angle(self, speed, angle):
        for smodule in self.swerve_modules:
            smodule.set_speed_and_angle(speed=speed, angle=angle)

    def update_speed(self, speed):
        for smodule in self.swerve_modules:
            smodule.set_speed(speed)

    def shutdown(self):
        ss.cleanup()
        self.killlist[0] = True