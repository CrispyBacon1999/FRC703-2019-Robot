import typing

import wpilib
import wpilib.drive

from magicbot import will_reset_to
from magicbot import tunable


class Drivetrain:
    train: wpilib.drive.MecanumDrive
    gyro: wpilib.ADXRS450_Gyro

    # Drive variables
    forward = will_reset_to(0)
    strafe = will_reset_to(0)
    rotate = will_reset_to(0)
    using_gyro = will_reset_to(False)
    current_angle = will_reset_to(0)
    target_angle = tunable(0)
    angle_diff = will_reset_to(0)

    # Multipliers
    forward_multiplier = tunable(1)
    strafe_multiplier = tunable(1)
    rotate_multiplier = tunable(1)

    gyro_rotate_to_angle_multiplier = tunable(1)

    slow_forward_multiplier = tunable(0.5)
    slow_strafe_multiplier = tunable(0.5)
    slow_rotate_multiplier = tunable(0.5)

    # PID

    # Angle
    angle_kp = 0.01
    angle_ki = 0
    angle_kd = 0
    angle_tolerance = 0.5

    def __init__(self):
        self.enabled = False

    def rotate_to_angle(self, angle):
        self.target_angle = angle
        self.using_gyro = True

    def move(
        self,
        forward: float,
        strafe: float,
        rotation: float,
        driver: bool = False,
        slow: bool = False,
        gyro: bool = False
    ):
        if driver:
            if slow:
                forward *= self.slow_forward_multiplier
                strafe *= self.slow_strafe_multiplier
                rotation *= self.slow_rotate_multiplier
            else:
                forward *= self.forward_multiplier
                strafe *= self.strafe_multiplier
                rotation *= self.rotate_multiplier
        else:
            if gyro:
                self.target_angle = rotation

        self.forward = forward
        self.strafe = strafe
        self.rotate = rotation
        self.using_gyro = gyro

    def execute(self):
        self.current_angle = self.gyro.getAngle()
        if self.using_gyro:
            self.angle_diff = self.target_angle - self.current_angle
            self.rotate = self.angle_diff * self.angle_kp
        self.train.driveCartesian(self.forward, self.strafe, self.rotate)
