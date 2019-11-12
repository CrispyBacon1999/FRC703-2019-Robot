from magicbot import AutonomousStateMachine, timed_state, state
import wpilib

from components.drivetrain import Drivetrain
from components.hatch import Hatch
from components.elevator import Elevator

from util import ROCKET_HATCH_HEIGHTS as HEIGHTS


class BottomFront(AutonomousStateMachine):
    MODE_NAME = "Bottom Front Rocket"
    DEFAULT = True

    drivetrain: Drivetrain
    elevator: Elevator
    hatch: Hatch

    @timed_state(duration=1, first=True, next_state="turn_to_tower")
    def drive_forward(self):
        self.elevator.hatch_mode()
        self.drivetrain.move(1, 0, 0)
        self.hatch.hold()

    @state()
    def turn_to_tower(self):
        target_angle = 30
        self.elevator.move_to_setpoint(HEIGHTS[0])
        self.drivetrain.rotate_to_angle(target_angle)
        self.drivetrain.using_gyro = True
        if abs(self.drivetrain.current_angle - target_angle) < 1e-3:
            self.next_state("drive_to_tower")

    @timed_state(duration=3, next_state="slide_sideways")
    def drive_to_tower(self):
        self.drivetrain.move(0.6, 0, 0)

    @timed_state(duration=1, next_state="align_to_tower")
    def slide_sideways(self):
        self.drivetrain.move(0, 0.6, 0)

    @timed_state(duration=0.4, next_state="place_hatch")
    def align_to_tower(self):
        self.drivetrain.move(0.3, 0, 0)
        self.hatch.lower()

    @timed_state(duration=1, next_state="back_away")
    def place_hatch(self):
        self.hatch.release()

    @timed_state(duration=1.5, next_state="rotate_to_loading")
    def back_away(self):
        self.drivetrain.move(-0.6, 0, -0.15)

    @state()
    def rotate_to_loading(self):

        target_angle = 180
        self.hatch.lift()

        self.drivetrain.rotate_to_angle(target_angle)
        self.drivetrain.using_gyro = True
        if abs(self.drivetrain.current_angle - target_angle) < 1e-3:
            self.next_state("drive_to_loading_station")

    @timed_state(duration=1.5)
    def drive_to_loading_station(self):
        self.drivetrain.move(1, -0.2, 0)
