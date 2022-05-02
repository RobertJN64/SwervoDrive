import json

def set_servo(pin, angle):
    pass #TODO - set servo

class MotorController:
    def __init__(self, pwPin: int, dirPin: int, spdPin: int):
        self.pwPin = pwPin
        self.dirPin = dirPin
        self.spdPin = spdPin

    def stop(self):
        pass # TODO - stop motor

    def set_motor_speed_and_direction(self, speed, motor_direction):
        pass #TODO - set motor speed and direction

class SwerveModule:
    def __init__(self, io_config: dict, servo_offset: int, inv_motor: bool):
        self.servoPin = io_config["servoPin"]
        self.motorController = MotorController(io_config['pwPin'], io_config['dirPin'], io_config['spdPin'])
        self.servo_offset = servo_offset
        self.inv_motor = inv_motor

    def stop(self):
        self.motorController.stop()

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

        set_servo(self.servoPin, angle)
        MotorController.set_motor_speed_and_direction(speed, motor_direction)

class Robot:
    def __init__(self):
        with open('robot_io.json') as f:
            robot_config = json.load(f)

        self.swerve_fr = SwerveModule(robot_config['swerve_fr'], servo_offset=0, inv_motor=False)
        self.swerve_fl = SwerveModule(robot_config['swerve_fl'], servo_offset=0, inv_motor=False)
        self.swerve_br = SwerveModule(robot_config['swerve_br'], servo_offset=180, inv_motor=True)
        self.swerve_bl = SwerveModule(robot_config['swerve_bl'], servo_offset=180, inv_motor=True)
        self.swerve_modules = [self.swerve_bl, self.swerve_br, self.swerve_fl, self.swerve_fr]

    def stop(self):
        for smodule in self.swerve_modules:
            smodule.stop()

    def robot_init(self):
        for smodule in self.swerve_modules:
            smodule.set_speed_and_angle(speed=0, angle=0)

    def set_all_modules_speed_and_angle(self, speed=0, angle=0):
        for smodule in self.swerve_modules:
            smodule.set_speed_and_angle(speed=speed, angle=angle)