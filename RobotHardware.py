class MotorController:
    def __int__(self, pwPin: int, dirPin: int, spdPin: int):
        self.pwPin = pwPin
        self.dirPin = dirPin
        self.spdPin = spdPin

class SwerveModule:
    def __init__(self, servoPin: int, motorController: MotorController, servoCenter: int, invMotor: bool):
        self.servoPin = servoPin
        self.motorController = motorController
        self.servoCenter = servoCenter
        self.invMotor = invMotor
