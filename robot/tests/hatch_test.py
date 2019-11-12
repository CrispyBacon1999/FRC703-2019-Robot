from magicbot.magic_tunable import setup_tunables
from components.hatch import Hatch

def test_lift():
    h = Hatch()
    setup_tunables(h, "Hatch")
    h.lift()
    assert h.is_in_position == False

def test_lower():
    h = Hatch()
    setup_tunables(h, "Hatch")
    h.lower()
    assert h.is_in_position == True

def test_hold():
    h = Hatch()
    setup_tunables(h, "Hatch")
    h.hold()
    assert h.is_holding == True

def test_release():
    h = Hatch()
    setup_tunables(h, "Hatch")
    h.release()
    assert h.is_holding == False