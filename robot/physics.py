from pyfrc.physics import drivetrains
import robotmap

class PhysicsEngine(object):
    def __init__(self, physics_controller):
        self.physics_controller = physics_controller
        self.position = 0
        self.physics_controller.add_device_gyro_channel("adxrs450_spi_0_angle")

    def update_sim(self, hal_data, now, tm_diff):
        lr_motor = hal_data["CAN"][f'sparkmax-{robotmap.DRIVE_MOTORS["rl"][0]}']["value"]
        lf_motor = hal_data["CAN"][f'sparkmax-{robotmap.DRIVE_MOTORS["fl"][0]}']["value"]
        rr_motor = hal_data["CAN"][f'sparkmax-{robotmap.DRIVE_MOTORS["rr"][0]}']["value"]
        rf_motor = hal_data["CAN"][f'sparkmax-{robotmap.DRIVE_MOTORS["fr"][0]}']["value"]

        vx, vy, vw = drivetrains.mecanum_drivetrain(
            lr_motor, rr_motor, lf_motor, rf_motor, speed=5
        )
        self.physics_controller.vector_drive(vx, vy, vw, tm_diff)

