# Drive Motor IDs
DRIVE_MOTORS = {
    "fl": [11, 12],
    "rl": [13, 14],
    "fr": [15, 16],
    "rr": [17, 18]
}


# Gyro
GYRO_ID = 19

# Elevator Piston IDs
ELEVATOR = {
    "brake": 1,
    "lower": 0,
    "motors": [
        21, 22
    ]
}

# Intake Piston IDs
INTAKE = {
    "cargo": {
        "actuator": 23,
        "lift": 1
    },
    "hatch": {
        "actuator": 2,
        "lift": 3
    }
}

# Camera Ports
CARGO_CAMERA_PORT = 0
HATCH_CAMERA_PORT = 1


# Climber
CLIMBER_FL = {
    "switch": {
        "top": 1,
        "bottom": 4
    },
    "motor": 24
}
CLIMBER_FR = {
    "switch": {
        "top": 2,
        "bottom": 5
    },
    "motor": 25
}
CLIMBER_BACK = {
    "switch": {
        "top": 3,
        "bottom": 6
    },
    "motor": 26
}

CLIMBER_WHEELS = 27
