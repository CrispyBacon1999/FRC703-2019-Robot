import typing

import wpilib
import wpilib.drive

from magicbot import will_reset_to
from magicbot import tunable


def xround(n):
    if round(n + 1) - round(n) == 1:
        return float(round(n))
    return n + abs(n) / n * 0.5

class Drivetrain:
    train: wpilib.drive.MecanumDrive
    gyro: wpilib.ADXRS450_Gyro

    # Drive variables
    forward = will_reset_to(0)
    strafe = will_reset_to(0)
    rotate = will_reset_to(0)
    using_gyro = will_reset_to(False)
    target_angle = tunable(0)

    # Multipliers
    forward_multiplier = tunable(1)
    strafe_multiplier = tunable(1)
    rotate_multiplier = tunable(1)

    gyro_rotate_to_angle_multiplier = tunable(2)

    slow_forward_multiplier = tunable(0.5)
    slow_strafe_multiplier = tunable(0.5)
    slow_rotate_multiplier = tunable(0.5)

    # PID

    # Angle
    angle_kp = 0.3
    angle_ki = 0
    angle_kd = 0
    angle_tolerance = 0.5

    def __init__(self):
        self.enabled = False

    @property
    def current_angle(self) -> float:
        return self.gyro.getAngle()

    @property
    def angle_difference(self) -> float:
        return self.target_angle - self.current_angle

    def rotate_to_angle(self, angle: float) -> None:
        self.target_angle = angle
        self.using_gyro = True

    def find_nearest_angle(self, target):
        curr = self.current_angle
        num_rots = curr/360
        # 360 relative
        rel = (curr + 180) % 360 - 180
        target = (target + 180) % 360 - 180
        diff = abs(target) - abs(rel)
        
        if abs(diff) > 180:
            if diff < 0:
                diff = target + 360 - curr
            else:
                diff = target - 360 - curr
        
        print(num_rots)
        return target + xround(num_rots) * 360
        
            

    @property
    def nearest_90(self):
        mod90 = self.current_angle % 90
        if mod90 > 45:
            return self.current_angle + mod90
        else:
            return self.current_angle - mod90

    def move(
        self,
        forward: float,
        strafe: float,
        rotation: float,
        driver: bool = False,
        slow: bool = False,
        gyro: bool = False,
        gyro_manually_set: bool = False,
    ):
        if driver:
            if slow:
                # Slow down the movement if the robot should be going slowly
                forward *= self.slow_forward_multiplier
                strafe *= self.slow_strafe_multiplier
                rotation *= self.slow_rotate_multiplier
            else:
                # Multiply inputs by the standard speed multipliers
                forward *= self.forward_multiplier
                strafe *= self.strafe_multiplier
                rotation *= self.rotate_multiplier
            if gyro and not gyro_manually_set:
                self.target_angle = (
                    rotation * self.gyro_rotate_to_angle_multiplier + self.current_angle
                )

        self.forward = forward
        self.strafe = strafe
        self.rotate = rotation
        self.using_gyro = gyro

    def execute(self):
        print(f"curr: {self.current_angle:.2f}, target: {self.target_angle:.2f}")
        if self.using_gyro:
            self.rotate = self.angle_difference * self.angle_kp
        self.train.driveCartesian(self.strafe, self.forward, self.rotate)
