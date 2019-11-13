from components.drivetrain import Drivetrain
from components.hatch import Hatch
from components.cargo import Cargo
from components.elevator import Elevator
from components.climber import Climber

from magicbot import StateMachine, state, timed_state

class Climb3(StateMachine):
    drivetrain: Drivetrain
    cargo: Cargo
    hatch: Hatch
    elevator: Elevator
    climber: Climber

    def climb(self):
        self.engage()
    
    def stop(self):
        self.done()

    @state(first=True, must_finish=True)
    def align_self(self):
        self.drivetrain.rotate_to_angle(180)
        self.cargo.lift()
        self.hatch.lift()
        self.elevator.move_to_setpoint(0)
        if abs(self.drivetrain.current_angle % 360 - 180) < 1e-3:
            self.next_state('press_into_hab') 
    
    @timed_state(duration=1.5, next_state='up',must_finish=True)
    def press_into_hab(self):
        self.drivetrain.move(.3, 0, 0)
    
    @state(must_finish=True)
    def up(self):
        self.climber.front_up()
        self.climber.rear_up()
        if self.climber.front_top_switch and self.climber.back_top_switch:
            self.next_state('lift_move_forward')

    @timed_state(duration=1.5, next_state='retract_front',must_finish=True)
    def lift_move_forward(self):
        self.climber.drive_forward()
        # Drop cargo and hatch to move weight forward as far as possible
        self.cargo.lower()
        self.hatch.lower()
        self.climber.front_up()
        self.climber.rear_up()
    
    @state(must_finish=True)
    def retract_front(self):
        self.climber.rear_up()
        self.climber.front_down()
        if self.climber.front_bottom_switch:
            self.next_state('push_to_platform')
    
    @timed_state(duration=3, next_state='retract_back',must_finish=True)
    def push_to_platform(self):
        self.climber.drive_forward()
        self.climber.rear_up()
        self.climber.front_down()
    
    @state(must_finish=True)
    def retract_back(self):
        self.climber.front_down()
        self.climber.rear_down()
        if self.climber.back_bottom_switch:
            self.next_state('push_to_wall')

    @timed_state(duration=.5,must_finish=True)
    def push_to_wall(self):
        self.hatch.lift()
        self.cargo.lift()
        self.drivetrain.move(.3, 0, 0)
        