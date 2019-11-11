from components.drivetrain import Drivetrain

from unittest.mock import patch, PropertyMock

def test_target_angle():
    dt = Drivetrain()
    with patch("components.drivetrain.Drivetrain.current_angle", new_callable=PropertyMock) as d:
        d.return_value = 360
        a = dt.find_nearest_angle(30)
        assert a == 390
