from enum import Enum

class AussenlichtState(Enum):
    OFF = 0
    ON = 1
    NO_ACTION = 2

class Evaluate:
    def __init__(self, TimeCache, now):
        self.TimeObject = TimeCache
        self.now = now

    def compute_aussenlicht_state(self):
        state = AussenlichtState.NO_ACTION
        to = self.TimeObject
        now = self.now
        if to.last_midnight < now < to.sunset:
            state = AussenlichtState.OFF
        elif to.sunset < now < to.midnight:
            state = AussenlichtState.ON
        else:
            print("No Action")
        return state