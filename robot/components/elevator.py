import wpilib
import ctre
import math

from .subcomponents.talon_encoder import TalonEncoder

from magicbot import tunable, will_reset_to, feedback


class Elevator:
    limit_switch_bottom: wpilib.DigitalInput
    motor1: ctre.TalonSRX
    motor2: ctre.TalonSRX
    encoder: TalonEncoder

    target_height = tunable(0)

    ticks_per_rot = tunable(4096)
    gear_ratio = tunable(0.75)

    height_for_cargo = tunable(False)
    height_for_hatch = tunable(False)

    cargo_height_const = tunable(4.0)
    hatch_height_const = tunable(12.5)
    pulley_radius = 1.375
    cable_to_elevator = 1.065

    encoder_height_ratio = tunable(0)

    i_err = 0

    height_kp = 0.5
    height_ki = 0.005
    height_kd = 0
    height_tolerance = 0.25

    @feedback
    def get_height(self):
        return self.current_height

    @property
    def current_height(self) -> float:
        return self.encoder.position * self.encoder_height_ratio
    
    @property
    def cargo_height(self) -> float:
        return self.current_height + self.cargo_height_const

    @property
    def hatch_height(self) -> float:
        return self.current_height + self.hatch_height_const

    def recalculate_ratio(self) -> None:
        self.encoder_height_ratio = (
            2
            * math.pi
            * self.gear_ratio
            * self.pulley_radius
            * self.cable_to_elevator
            / self.ticks_per_rot
        )

    def move_to_setpoint(self, setpoint: float):
        if setpoint >= 0 or setpoint < self.max_height:
            self.target_height = setpoint

    def hatch_mode(self):
        self.height_for_hatch = True
        self.height_for_cargo = False
    
    def cargo_mode(self):
        self.height_for_cargo = True
        self.height_for_hatch = False

    def stop(self):
        self.target_height = self.current_height

    def execute(self):
        if self.limit_switch_bottom.get():
            self.encoder.reset()
        
        # Calculate Target Height for cargo or hatch
        target = self.target_height
        current = self.current_height
        if self.height_for_cargo:
            target = self.target_height + self.cargo_height_const
            current = self.cargo_height
        elif self.height_for_hatch:
            target = self.target_height + self.hatch_height_const
            current = self.hatch_height
        
        error = target - current
        p = error * self.height_kp
        if abs(error) > self.height_tolerance:
            self.i_err += error
        else:
            self.i_err = 0

        pid_output = p + self.i_err * self.height_ki


        self.motor1.set(ctre.ControlMode.PercentOutput, pid_output)
