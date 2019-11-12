from magicbot.magic_tunable import setup_tunables
from components.elevator import Elevator

from unittest.mock import patch, PropertyMock

def test_setpoint():
    e = Elevator()
    setup_tunables(e, "Elevator")
    
    e.move_to_setpoint(0)
    assert e.target_height == 0, "Target height should be set to the value"

    e.move_to_setpoint(30)
    assert e.target_height == 30, "Target height should be set to the value"

    e.move_to_setpoint(e.max_height + 50)
    assert e.target_height == e.max_height, "Target height should be the max height"

    e.move_to_setpoint(-5)
    assert e.target_height == 0, "Target height should be the minimum value"

def test_get_height():
    e = Elevator()
    setup_tunables(e, "Elevator") 
    with patch(
        "components.elevator.Elevator.current_height", new_callable=PropertyMock
    ) as ch:
        ch.return_value = 50
        assert e.get_height() == e.current_height

def test_current_height():
    e = Elevator()
    setup_tunables(e, "Elevator") 
    with patch(
        "components.elevator.Elevator.encoder.position", new_callable=PropertyMock
    ) as ep:
        ep.return_value = 4096
        assert e.current_height == 4096 * e.encoder_height_ratio

def test_cargo_height():
    e = Elevator()
    setup_tunables(e, "Elevator") 
    with patch(
        "components.elevator.Elevator.current_height", new_callable=PropertyMock
    ) as ch:
        ch.return_value = 50
        assert e.cargo_height == 50 + e.cargo_height_const

def test_hatch_height():
    e = Elevator()
    setup_tunables(e, "Elevator") 
    with patch(
        "components.elevator.Elevator.current_height", new_callable=PropertyMock
    ) as ch:
        ch.return_value = 50
        assert e.hatch_height == 50 + e.hatch_height_const