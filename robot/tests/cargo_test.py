from magicbot.magic_tunable import setup_tunables
from components.cargo import Cargo

def test_lift():
    c = Cargo()
    setup_tunables(c, "Cargo")
    c.lift()
    assert c.is_in_position == False

def test_lower():
    c = Cargo()
    setup_tunables(c, "Cargo")
    c.lower()
    assert c.is_in_position == True

def test_intake():
    c = Cargo()
    setup_tunables(c, "Cargo")
    c.intake()
    assert c.motor_speed == c.motor_input_speed

def test_outtake():
    c = Cargo()
    setup_tunables(c, "Cargo")
    c.outtake()
    assert c.motor_speed == c.motor_output_speed