import wpilib
import ctre
from .encoder import Encoder

class TalonEncoder(Encoder):

    attached_motor: ctre.TalonSRX

    def __init__(self, attachedMotor: ctre.TalonSRX, inverted=False):
        super().__init__(inverted)

        self.attached_motor = attachedMotor
        self.attached_motor.configSelectedFeedbackSensor(ctre.FeedbackDevice.CTRE_MagEncoder_Relative)
    
    @property
    def raw_position(self):
        return (-1 if self.inverted else 1) * self.attached_motor.getSelectedSensorPosition()
    
    def hard_reset(self):
        self.attached_motor.setQuadraturePosition(0)
        self.zero_position = self.raw_position
    
    @property
    def velocity(self):
        return (-1 if self.inverted else 1) * self.attached_motor.getSelectedSensorVelocity()