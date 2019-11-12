from magicbot import tunable, will_reset_to
import wpilib


class Hatch:

    lift_piston = wpilib.Solenoid
    hold_piston = wpilib.Solenoid

    is_holding = tunable(False)
    is_in_position = tunable(False)

    def lift(self):
        self.is_in_position = False

    def lower(self):
        self.is_in_position = True

    def hold(self):
        self.is_holding = True

    def release(self):
        self.is_holding = False

    def execute(self):
        self.lift_piston.set(self.is_in_position)
        self.hold_piston.set(self.is_holding)
