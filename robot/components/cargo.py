from magicbot import tunable, will_reset_to
import wpilib
import ctre


class Cargo:

    lift_piston = wpilib.Solenoid
    motor = ctre.TalonSRX

    motor_speed = will_reset_to(0)

    is_in_position = tunable(False)

    motor_input_speed = tunable(-.6)
    motor_output_speed = tunable(1)

    def lift(self):
        self.is_in_position = False

    def lower(self):
        self.is_in_position = True

    def intake(self):
        self.motor_speed = self.motor_input_speed
    
    def outtake(self):
        self.motor_speed = self.motor_output_speed

    def execute(self):
        self.motor.set(ctre.ControlMode.PercentOutput,self.motor_speed)