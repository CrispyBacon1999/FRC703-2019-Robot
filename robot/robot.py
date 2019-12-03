import wpilib
from wpilib.buttons import JoystickButton
import magicbot
import ctre
import rev
import robotmap

from components.cargo import Cargo
from components.climber import Climber
from components.drivetrain import Drivetrain
from components.elevator import Elevator
from components.hatch import Hatch
from components.trajectory_follower import TrajectoryFollower

from automations.climb3 import Climb3

from components.subcomponents.talon_encoder import TalonEncoder
from util import ROCKET_CARGO_HEIGHTS, ROCKET_HATCH_HEIGHTS

from trajectory_generator import load_trajectories

class DeepSpaceRobot(magicbot.MagicRobot):

    # state machines

    climb3: Climb3

    # components

    cargo: Cargo
    climber: Climber
    drivetrain: Drivetrain
    elevator: Elevator
    hatch: Hatch
    follower: TrajectoryFollower

    drive_joystick: wpilib.Joystick

    def createObjects(self):

        # Drivetrain
        self.motor_fl0 = rev.CANSparkMax(
            robotmap.DRIVE_MOTORS["fl"][0], rev.MotorType.kBrushless
        )  # 11
        self.motor_fr0 = rev.CANSparkMax(
            robotmap.DRIVE_MOTORS["fr"][0], rev.MotorType.kBrushless
        )  # 15
        self.motor_rl0 = rev.CANSparkMax(
            robotmap.DRIVE_MOTORS["rl"][0], rev.MotorType.kBrushless
        )  # 13
        self.motor_rr0 = rev.CANSparkMax(
            robotmap.DRIVE_MOTORS["rr"][0], rev.MotorType.kBrushless
        )  # 17

        self.motor_rr0.setInverted(True)
        self.motor_fr0.setInverted(True)

        # Set Motors to follow each other
        # Ignore secondary motors for simulation, not fully supported yet
        if not self.isSimulation():
            self.motor_fr1 = rev.CANSparkMax(
                robotmap.DRIVE_MOTORS["fr"][1], rev.MotorType.kBrushless
            )
            self.motor_fl1 = rev.CANSparkMax(
                robotmap.DRIVE_MOTORS["fl"][1], rev.MotorType.kBrushless
            )
            self.motor_rl1 = rev.CANSparkMax(
                robotmap.DRIVE_MOTORS["rl"][1], rev.MotorType.kBrushless
            )
            self.motor_rr1 = rev.CANSparkMax(
                robotmap.DRIVE_MOTORS["rr"][1], rev.MotorType.kBrushless
            )
            self.motor_fl1.follow(self.motor_fl0)
            self.motor_fr1.follow(self.motor_fr0)
            self.motor_rl1.follow(self.motor_rl0)
            self.motor_rr1.follow(self.motor_rr0)

        self.drivetrain_train = wpilib.drive.MecanumDrive(
            self.motor_fl0, self.motor_rl0, self.motor_fr0, self.motor_rr0
        )

        self.drivetrain_gyro = wpilib.ADXRS450_Gyro()

        # Elevator
        self.elevator_motor1 = ctre.TalonSRX(robotmap.ELEVATOR["motors"][0])
        self.elevator_motor2 = ctre.TalonSRX(robotmap.ELEVATOR["motors"][1])
        self.elevator_motor2.follow(self.elevator_motor1)
        self.elevator_limit_switch_bottom = wpilib.DigitalInput(
            robotmap.ELEVATOR["lower"]
        )
        self.elevator_encoder = TalonEncoder(self.elevator_motor1)

        # Hatch
        self.hatch_hold_piston = wpilib.Solenoid(robotmap.INTAKE["hatch"]["actuator"])
        self.hatch_lift_piston = wpilib.Solenoid(robotmap.INTAKE["hatch"]["lift"])

        # Cargo
        self.cargo_motor = ctre.TalonSRX(robotmap.INTAKE["cargo"]["actuator"])
        self.cargo_lift_piston = wpilib.Solenoid(robotmap.INTAKE["cargo"]["lift"])

        # Climber
        self.climber_front_left_motor = ctre.VictorSPX(robotmap.CLIMBER_FL["motor"])
        self.climber_front_right_motor = ctre.VictorSPX(robotmap.CLIMBER_FR["motor"])
        self.climber_back_motor = ctre.VictorSPX(robotmap.CLIMBER_BACK["motor"])
        self.climber_wheel_motor = ctre.VictorSPX(robotmap.CLIMBER_WHEELS)

        # Climber Limit Switches
        self.climber_front_left_upper_switch = wpilib.DigitalInput(
            robotmap.CLIMBER_FL["switch"]["top"]
        )
        self.climber_front_right_upper_switch = wpilib.DigitalInput(
            robotmap.CLIMBER_FR["switch"]["top"]
        )
        self.climber_front_left_lower_switch = wpilib.DigitalInput(
            robotmap.CLIMBER_FL["switch"]["bottom"]
        )
        self.climber_front_right_lower_switch = wpilib.DigitalInput(
            robotmap.CLIMBER_FR["switch"]["bottom"]
        )
        self.climber_back_upper_switch = wpilib.DigitalInput(
            robotmap.CLIMBER_BACK["switch"]["top"]
        )
        self.climber_back_lower_switch = wpilib.DigitalInput(
            robotmap.CLIMBER_BACK["switch"]["bottom"]
        )

        self.trajectories = load_trajectories()



        # Joystick 1
        self.drive_joystick = wpilib.Joystick(0)
        
        self.slow_button = JoystickButton(self.drive_joystick, 1)
        self.bottom_tower_front_button = JoystickButton(self.drive_joystick, 9)
        self.bottom_tower_back_button = JoystickButton(self.drive_joystick, 10)
        self.perp_button = JoystickButton(self.drive_joystick, 6)
        self.top_tower_front_button = JoystickButton(self.drive_joystick, 7)
        self.top_tower_back_button = JoystickButton(self.drive_joystick, 8)

        self.climb_button = JoystickButton(self.drive_joystick, 3)
        self.climb_cancel_button = JoystickButton(self.drive_joystick, 4)


        # Joystick 2
        self.op_joystick = wpilib.Joystick(1)

        self.tower_l1_button = JoystickButton(self.op_joystick, 1)
        self.tower_l2_button = JoystickButton(self.op_joystick, 2)
        self.tower_l3_button = JoystickButton(self.op_joystick, 3)
        self.hatch_panel_button = JoystickButton(self.op_joystick, 5)
        self.cargo_ball_button = JoystickButton(self.op_joystick, 6)
        self.elevator_ground_button = JoystickButton(self.op_joystick, 7)
        self.elevator_load_button = JoystickButton(self.op_joystick, 4)

        # Climb Joystick
        self.climb_joystick = wpilib.Joystick(2)
        self.climber_front_lift_button = JoystickButton(self.climb_joystick, 1)
        self.climber_back_lift_button = JoystickButton(self.climb_joystick, 2)
        self.climber_front_lower_button = JoystickButton(self.climb_joystick, 3)
        self.climber_back_lower_button = JoystickButton(self.climb_joystick, 4)
        self.climber_drive_button = JoystickButton(self.climb_joystick, 5)
        self.climber_reverse_button = JoystickButton(self.climb_joystick, 6)

    def teleopInit(self):
        self.elevator.recalculate_ratio()
        self.elevator.cargo_mode()

    def teleopPeriodic(self):
        # Standard Mecanum Driving
        forward = -self.drive_joystick.getY()
        strafe = self.drive_joystick.getX()
        turn = self.drive_joystick.getRawAxis(3)
        slow = self.slow_button.get()
        gyro_manually_set = False

        # Auto Rotation

        if self.top_tower_front_button.get():
            self.drivetrain.rotate_to_angle(self.drivetrain.find_nearest_angle(-30))
            gyro_manually_set = True
        elif self.bottom_tower_front_button.get():
            self.drivetrain.rotate_to_angle(self.drivetrain.find_nearest_angle(30))
            gyro_manually_set = True
        elif self.bottom_tower_back_button.get():
            self.drivetrain.rotate_to_angle(self.drivetrain.find_nearest_angle(150))
            gyro_manually_set = True
        elif self.top_tower_back_button.get():
            self.drivetrain.rotate_to_angle(self.drivetrain.find_nearest_angle(-150))
            gyro_manually_set = True
        elif self.perp_button.get():
            self.drivetrain.rotate_to_angle(self.drivetrain.nearest_90)
            gyro_manually_set = True

        HEIGHTS = [0, 0, 0]
        if self.hatch_panel_button.get():
            self.elevator.hatch_mode()
        elif self.cargo_ball_button.get():
            self.elevator.cargo_mode()

        if self.elevator.height_for_hatch:
            HEIGHTS = ROCKET_HATCH_HEIGHTS
        elif self.elevator.height_for_cargo:
            HEIGHTS = ROCKET_CARGO_HEIGHTS
        if self.tower_l1_button.get():
            self.elevator.move_to_setpoint(HEIGHTS[0])
        elif self.tower_l2_button.get():
            self.elevator.move_to_setpoint(HEIGHTS[1])
        elif self.tower_l3_button.get():
            self.elevator.move_to_setpoint(HEIGHTS[2])
        elif self.elevator_load_button.get():
            self.elevator.move_to_setpoint(
                ROCKET_HATCH_HEIGHTS[0] if self.elevator.height_for_hatch else 0
            )
        
        if self.climber_front_lift_button.get():
            self.climber.front_up()
        if self.climber_back_lift_button.get():
            self.climber.rear_up()
        if self.climber_front_lower_button.get():
            self.climber.front_down()
        if self.climber_back_lower_button.get():
            self.climber.rear_down()
        if self.climber_drive_button.get():
            self.climber.drive_forward()
        if self.climber_reverse_button.get():
            self.climber.drive_backwards()

        if self.climb_button.get():
            self.climb3.climb()
        if self.climb_cancel_button.get():
            self.climb3.stop()

        self.drivetrain.move(
            forward,
            strafe,
            turn,
            gyro=True,
            driver=True,
            slow=slow,
            gyro_manually_set=gyro_manually_set,
        )

    def disabledInit(self):
        # Set everything to the state it should be in for being disabled
        self.elevator.recalculate_ratio()
        self.drivetrain.move(0, 0, 0)
        self.elevator.stop()


if __name__ == "__main__":
    wpilib.run(DeepSpaceRobot)
