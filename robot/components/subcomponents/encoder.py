import typing


class Encoder:
    zero_position = 0
    inverted = False
    direction_scaler = 1

    def __init__(self, inverted):
        self.inverted = inverted
        self.direction_scaler = -1.0 if self.inverted else 1.0

    @property
    def raw_position(self) -> float:
        pass

    @property
    def position(self):
        return self.raw_position - self.zero_position

    @property
    def velocity(self):
        pass

    def reset(self):
        self.zero_position = self.raw_position

    def hard_reset(self):
        pass
