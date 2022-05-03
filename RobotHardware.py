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

    def set_speed(self, speed):
        pass #TODO - set speed, start motor

    def set_motor_speed_and_direction(self, speed, motor_direction):
        # TODO - set direction
        self.set_speed(speed)

class SwerveModule:
    def __init__(self, io_config: dict, servo_offset: int, inv_motor: bool):
        self.servoPin = io_config["servoPin"]
        self.motorController = MotorController(io_config['pwPin'], io_config['dirPin'], io_config['spdPin'])
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

        set_servo(self.servoPin, angle)
        self.motorController.set_motor_speed_and_direction(speed, motor_direction)

        self.current_motor_direction = motor_direction

        if self.inv_motor:
            self.current_motor_direction = not self.current_motor_direction

        self.current_angle = angle + self.servo_offset
        self.current_speed = speed

    def get_info(self):
        return self.current_angle, self.current_motor_direction, self.current_speed

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

    def set_all_modules_speed_and_angle(self, speed, angle):
        for smodule in self.swerve_modules:
            smodule.set_speed_and_angle(speed=speed, angle=angle)

    def update_speed(self, speed):
        for smodule in self.swerve_modules:
            smodule.set_speed(speed)