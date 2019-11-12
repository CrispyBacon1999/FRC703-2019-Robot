from pyfrc.physics import drivetrains
import robotmap


class PhysicsEngine(object):
    def __init__(self, physics_controller):
        self.physics_controller = physics_controller
        self.position = 0
        self.physics_controller.add_device_gyro_channel("adxrs450_spi_0_angle")
        self.elevator_encoder_ticks_per_sec = 4096 / 2

    def update_sim(self, hal_data, now, tm_diff):
        lr_motor = hal_data["CAN"][f'sparkmax-{robotmap.DRIVE_MOTORS["rl"][0]}'][
            "value"
        ]
        lf_motor = hal_data["CAN"][f'sparkmax-{robotmap.DRIVE_MOTORS["fl"][0]}'][
            "value"
        ]
        rr_motor = hal_data["CAN"][f'sparkmax-{robotmap.DRIVE_MOTORS["rr"][0]}'][
            "value"
        ]
        rf_motor = hal_data["CAN"][f'sparkmax-{robotmap.DRIVE_MOTORS["fr"][0]}'][
            "value"
        ]
        elevator_motor = hal_data["CAN"][robotmap.ELEVATOR["motors"][0]]
        elevator_last_pos = elevator_motor["quad_position"]
        elevator_last_vel = elevator_motor["quad_velocity"]
        elevator_curr_set = elevator_motor["value"]
        tick_diff = self.elevator_encoder_ticks_per_sec * tm_diff
        # Account for natural drift as well
        if elevator_last_pos > 200:
            hal_data["CAN"][robotmap.ELEVATOR["motors"][0]]["quad_position"] = (
                int(elevator_last_pos + tick_diff * elevator_curr_set) - 5
            )
        else:

            hal_data["CAN"][robotmap.ELEVATOR["motors"][0]]["quad_position"] = int(
                elevator_last_pos + tick_diff * elevator_curr_set
            )

        vx, vy, vw = drivetrains.mecanum_drivetrain(
            lr_motor, rr_motor, lf_motor, rf_motor, speed=5
        )
        self.physics_controller.vector_drive(vx, vy, vw, tm_diff)
