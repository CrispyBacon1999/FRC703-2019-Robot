from magicbot import AutonomousStateMachine, state
import wpilib

from components.drivetrain import Drivetrain
from components.trajectory_follower import TrajectoryFollower

class Charge(AutonomousStateMachine):
    MODE_NAME = 'Charge'
    drivetrain: Drivetrain
    follower: TrajectoryFollower

    @state(first=True)
    def charge(self, initial_call):
        if initial_call:
            self.follower.follow_trajectory('charge')
        
        if not self.follower.is_following('charge'):
            self.done()