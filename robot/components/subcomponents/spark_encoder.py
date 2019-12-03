import wpilib
import rev
from .encoder import Encoder

class SparkEncoder(Encoder):

    attached_motor: rev.CANSparkMax

    
    def __init__(self, attached_motor: rev.CANSparkMax, inverted=False):
        super().__init__(inverted)
        self.attached_motor = attached_motor
    
    @property
    def raw_position(self):
        return (
            -1 if self.inverted else 1
        ) * self.attached_motor.getEncoder().getPosition()
    
    def hard_reset(self):
        self.attached_motor.getEncoder().setPosition(0)
        self.zero_position = self.raw_position
    
    @property
    def velocity(self):
        return (
            -1 if self.inverted else 1
        ) * self.attached_motor.getEncoder().getVelocity()