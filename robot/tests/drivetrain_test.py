from components.drivetrain import Drivetrain
from magicbot.magic_tunable import setup_tunables

from unittest.mock import patch, PropertyMock


def test_nearest_angle():
    dt = Drivetrain()
    setup_tunables(dt, "Drivetrain")
    with patch(
        "components.drivetrain.Drivetrain.current_angle", new_callable=PropertyMock
    ) as d:
        d.return_value = 360
        a = dt.find_nearest_angle(30)
        assert a == 390


def test_angle_difference():
    dt = Drivetrain()
    setup_tunables(dt, "Drivetrain")
    with patch(
        "components.drivetrain.Drivetrain.current_angle", new_callable=PropertyMock
    ) as d:
        d.return_value = 360
        dt.target_angle = 390
        a = dt.angle_difference
        assert a == 30


def test_rotate_to_angle():
    dt = Drivetrain()
    setup_tunables(dt, "Drivetrain")
    dt.rotate_to_angle(80)
    assert dt.target_angle == 80
    assert dt.using_gyro == True


def test_nearest_90():
    dt = Drivetrain()
    setup_tunables(dt, "Drivetrain")
    with patch(
        "components.drivetrain.Drivetrain.current_angle", new_callable=PropertyMock
    ) as d:
        d.return_value = 50
        a = dt.nearest_90
        assert a == 90


def test_move():
    dt = Drivetrain()
    setup_tunables(dt, "Drivetrain")
    with patch(
        "components.drivetrain.Drivetrain.current_angle", new_callable=PropertyMock
    ) as d:
        d.return_value = 30
        dt.move(1, 0, 0, driver=False, slow=False, gyro=False, gyro_manually_set=False)
        assert (
            dt.forward == 1 * dt.forward_multiplier
            and dt.strafe == 0 * dt.strafe_multiplier
            and dt.rotate == 0 * dt.rotate_multiplier
        )
        dt.move(0, 0, 1, driver=True, slow=False, gyro=True, gyro_manually_set=False)
        assert (
            dt.forward == 0 * dt.forward_multiplier
            and dt.strafe == 0 * dt.strafe_multiplier
            and dt.rotate == 1
            and dt.target_angle
            == 1 * dt.gyro_rotate_to_angle_multiplier + dt.current_angle
        )
