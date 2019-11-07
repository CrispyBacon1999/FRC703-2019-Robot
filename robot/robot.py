import wpilib
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

    def createObjects(self):
        self.motor_fl0 = rev.CANSparkMax(robotmap.DRIVE_MOTORS["fl"][0], rev.MotorType.kBrushless)
        self.motor_fl1 = rev.CANSparkMax(robotmap.DRIVE_MOTORS["fl"][1], rev.MotorType.kBrushless)
        self.motor_fr0 = rev.CANSparkMax(robotmap.DRIVE_MOTORS["fr"][0], rev.MotorType.kBrushless)
        self.motor_fr1 = rev.CANSparkMax(robotmap.DRIVE_MOTORS["fr"][1], rev.MotorType.kBrushless)
        self.motor_rl0 = rev.CANSparkMax(robotmap.DRIVE_MOTORS["rl"][0], rev.MotorType.kBrushless)
        self.motor_rl1 = rev.CANSparkMax(robotmap.DRIVE_MOTORS["rl"][1], rev.MotorType.kBrushless)
        self.motor_rr0 = rev.CANSparkMax(robotmap.DRIVE_MOTORS["rr"][0], rev.MotorType.kBrushless)
        self.motor_rr1 = rev.CANSparkMax(robotmap.DRIVE_MOTORS["rr"][1], rev.MotorType.kBrushless)

        # Set Motors to follow each other
        if not self.isSimulation():
            self.motor_fl1.follow(self.motor_fl0)
            self.motor_fr1.follow(self.motor_fr0)
            self.motor_rl1.follow(self.motor_rl0)
            self.motor_rr1.follow(self.motor_rr0)

        self.drivetrain_train = wpilib.drive.MecanumDrive(
            self.motor_fl0, self.motor_rl0, self.motor_fr0, self.motor_rr0
        )

        self.drivetrain_gyro = wpilib.ADXRS450_Gyro()

    def teleopInit(self):
        pass

    def teleopPeriodic(self):
        self.drivetrain.move(.01, 0, .5, gyro=True, driver=True)

    def disabledInit(self):
        # Set everything to the state it should be in for being disabled
        pass


if __name__ == "__main__":
    wpilib.run(DeepSpaceRobot)
