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


class DeepSpaceRobot(magicbot.MagicRobot):
    # cargo: Cargo
    # climber: Climber
    drivetrain: Drivetrain
    # elevator: Elevator
    # hatch: Hatch

    drive_joystick: wpilib.Joystick

    def createObjects(self):
        self.motor_fl0 = rev.CANSparkMax(robotmap.DRIVE_MOTORS["fl"][0], rev.MotorType.kBrushless) # 11
        self.motor_fr0 = rev.CANSparkMax(robotmap.DRIVE_MOTORS["fr"][0], rev.MotorType.kBrushless) # 15
        self.motor_rl0 = rev.CANSparkMax(robotmap.DRIVE_MOTORS["rl"][0], rev.MotorType.kBrushless) # 13
        self.motor_rr0 = rev.CANSparkMax(robotmap.DRIVE_MOTORS["rr"][0], rev.MotorType.kBrushless) # 17

        self.motor_rr0.setInverted(True)
        self.motor_fr0.setInverted(True)
        

        # Set Motors to follow each other
        # Ignore secondary motors for simulation, not fully supported yet
        if not self.isSimulation():
            self.motor_fr1 = rev.CANSparkMax(robotmap.DRIVE_MOTORS["fr"][1], rev.MotorType.kBrushless)
            self.motor_fl1 = rev.CANSparkMax(robotmap.DRIVE_MOTORS["fl"][1], rev.MotorType.kBrushless)
            self.motor_rl1 = rev.CANSparkMax(robotmap.DRIVE_MOTORS["rl"][1], rev.MotorType.kBrushless)
            self.motor_rr1 = rev.CANSparkMax(robotmap.DRIVE_MOTORS["rr"][1], rev.MotorType.kBrushless)
            self.motor_fl1.follow(self.motor_fl0)
            self.motor_fr1.follow(self.motor_fr0)
            self.motor_rl1.follow(self.motor_rl0)
            self.motor_rr1.follow(self.motor_rr0)

        self.drivetrain_train = wpilib.drive.MecanumDrive(
            self.motor_fl0, self.motor_rl0, self.motor_fr0, self.motor_rr0
        )

        self.drivetrain_gyro = wpilib.ADXRS450_Gyro()
        self.drive_joystick = wpilib.Joystick(0)
        self.slow_button = JoystickButton(self.drive_joystick, 1)
        self.bottom_tower_front_button = JoystickButton(self.drive_joystick, 9)
        self.bottom_tower_back_button = JoystickButton(self.drive_joystick, 10)
        self.bottom_tower_button = JoystickButton(self.drive_joystick, 6)
        self.top_tower_button = JoystickButton(self.drive_joystick, 5)
        self.top_tower_front_button = JoystickButton(self.drive_joystick, 7)
        self.top_tower_back_button = JoystickButton(self.drive_joystick, 8)

    def teleopInit(self):
        pass

    
    def teleopPeriodic(self):
        forward = -self.drive_joystick.getY()
        strafe = self.drive_joystick.getX()
        turn = self.drive_joystick.getRawAxis(3)
        slow = self.slow_button.get()
        gyro_manually_set = False
        if self.top_tower_front_button.get():
            self.drivetrain.rotate_to_angle(-30)
            gyro_manually_set = True
        elif self.bottom_tower_front_button.get():
            self.drivetrain.rotate_to_angle(30)
            gyro_manually_set = True
        elif self.bottom_tower_back_button.get():
            self.drivetrain.rotate_to_angle(150)
            gyro_manually_set = True
        elif self.top_tower_back_button.get():
            self.drivetrain.rotate_to_angle(-150)
            gyro_manually_set = True
        elif self.top_tower_button.get():
            self.drivetrain.rotate_to_angle(-90)
            gyro_manually_set = True
        elif self.bottom_tower_button.get():
            self.drivetrain.rotate_to_angle(90)
            gyro_manually_set = True
        self.drivetrain.move(forward, strafe, turn, gyro=True, driver=True, slow=slow, gyro_manually_set=gyro_manually_set)
        # self.drivetrain.move(1, 0, 0, gyro=True, driver=False)
    

    def disabledInit(self):
        # Set everything to the state it should be in for being disabled
        pass


if __name__ == "__main__":
    wpilib.run(DeepSpaceRobot)
