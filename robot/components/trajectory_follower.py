import pathfinder as pf
import wpilib
from wpilib import drive
from components.drivetrain import Drivetrain
from magicbot.magic_tunable import tunable
from ctre import TalonSRX

class TrajectoryFollower:
    WHEEL_DIAMETER = 4
    KV = tunable(1.02)
    KA = tunable(0.003)
    ANGLE_CONST = tunable(0.8)
    KENCODER_TICKS = 42

    drivetrain: Drivetrain
    

    trajectories: dict

    def on_enable(self):
        self.current_trajectory = None
        # self.last_difference = 0
        self.left_follower = pf.followers.EncoderFollower(None)
        self.right_follower = pf.followers.EncoderFollower(None)
        self.left_follower.configurePIDVA(1.0, 0, 0, self.KV, self.KA)
        self.right_follower.configurePIDVA(1.0, 0, 0, self.KV, self.KA)

        self._configure_encoders()


    def _configure_encoders(self):
        self.drivetrain.r_encoder.reset()
        self.drivetrain.l_encoder.reset()
        self.left_follower.configureEncoder(self.drivetrain.left_encoder, self.KENCODER_TICKS, self.WHEEL_DIAMETER)
        self.right_follower.configureEncoder(self.drivetrain.right_encoder, self.KENCODER_TICKS, self.WHEEL_DIAMETER)


    def follow_trajectory(self, trajectory_name: str):
        self.current_trajectory = trajectory_name
        self.left_follower.setTrajectory(self.trajectories[trajectory_name][0])
        self.right_follower.setTrajectory(self.trajectories[trajectory_name][1])
        self._configure_encoders()

    def is_following(self, trajectory_name):
        return self.current_trajectory is not None and self.current_trajectory == trajectory_name

    def execute(self):
        left = self.left_follower.calculate(self.drivetrain.left_encoder)
        right = self.right_follower.calculate(self.drivetrain.right_encoder)
        desired_heading = pf.r2d(
            self.left_follower.getHeading()
        )
        angleDifference = pf.boundHalfDegrees(desired_heading - self.drivetrain.current_angle)
        turn = self.ANGLE_CONST * (-1.0/80.0) * angleDifference
        left += turn
        right -= turn

        self.drivetrain.move_tank(left, right)

        if wpilib.RobotBase.isSimulation():
            from pyfrc.sim import get_user_renderer
            renderer = get_user_renderer()
            if renderer:
                renderer.draw_pathfinder_trajectory(
                    self.trajectories[trajectory_name][0],
                    color="#0000ff", offset=(-1,0)
                )
                renderer.draw_pathfinder_trajectory(
                    self.trajectories[trajectory_name][1],
                    color="#0000ff", offset=(1,0)
                )