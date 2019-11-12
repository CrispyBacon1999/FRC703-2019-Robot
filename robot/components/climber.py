import typing

import ctre
import wpilib
from magicbot import tunable, will_reset_to


class Climber:

    wheel_motor = ctre.VictorSPX
    wheel_speed = will_reset_to(0)

    wheel_speed_const = 1

    front_left_speed = will_reset_to(0)
    front_right_speed = will_reset_to(0)
    back_speed = will_reset_to(0)

    front_left_motor: ctre.VictorSPX
    front_right_motor: ctre.VictorSPX
    back_motor: ctre.VictorSPX

    front_left_upper_switch: wpilib.DigitalInput
    front_right_upper_switch: wpilib.DigitalInput
    front_left_lower_switch: wpilib.DigitalInput
    front_right_lower_switch: wpilib.DigitalInput
    back_upper_switch: wpilib.DigitalInput
    back_lower_switch: wpilib.DigitalInput

    front_speed_const = 0.8
    back_speed_const = 0.8

    def compute_speed(
        self,
        speed: float,
        upper_switch: wpilib.DigitalInput,
        lower_switch: wpilib.DigitalInput,
    ) -> float:
        if not upper_switch.get() and speed > 0:
            return speed
        elif not lower_switch.get() and speed < 0:
            return speed
        else:
            return 0

    @property
    def front_top_switch(self):
        return self.front_left_upper_switch.get() and self.front_right_upper_switch.get()
    
    @property
    def front_bottom_switch(self):
        return self.front_left_lower_switch.get() and self.front_right_lower_switch.get()

    @property
    def back_top_switch(self):
        return self.back_upper_switch.get()

    @property
    def back_bottom_switch(self):
        return self.back_lower_switch.get()

    def drive_forward(self):
        self.wheel_speed = self.wheel_speed_const
    
    def drive_backwards(self):
        self.wheel_speed = -self.wheel_speed_const

    def front_up(self):
        self.front_left_speed = self.compute_speed(
            self.front_speed_const,
            self.front_left_upper_switch,
            self.front_left_lower_switch,
        )
        self.front_right_speed = self.compute_speed(
            self.front_speed_const,
            self.front_right_upper_switch,
            self.front_right_lower_switch,
        )

    def front_down(self):
        self.front_left_speed = self.compute_speed(
            -self.front_speed_const,
            self.front_left_upper_switch,
            self.front_left_lower_switch,
        )
        self.front_right_speed = self.compute_speed(
            -self.front_speed_const,
            self.front_right_upper_switch,
            self.front_right_lower_switch,
        )

    def rear_up(self):
        self.back_speed = self.compute_speed(
            self.back_speed_const,
            self.back_upper_switch,
            self.back_lower_switch,
        )

    def rear_down(self):
        self.back_speed = self.compute_speed(
            -self.back_speed_const,
            self.back_upper_switch,
            self.back_lower_switch,
        )

    def execute(self):
        self.front_left_motor.set(ctre.ControlMode.PercentOutput, self.front_left_speed)
        self.front_right_motor.set(ctre.ControlMode.PercentOutput, self.front_right_speed)
        self.back_motor.set(ctre.ControlMode.PercentOutput, self.back_speed)
        self.wheel_motor.set(ctre.ControlMode.PercentOutput, self.wheel_speed)
