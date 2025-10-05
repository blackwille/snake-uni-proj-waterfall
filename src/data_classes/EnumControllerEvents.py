from enum import Enum


class ControllerEvent(Enum):
    MOVE_UP = 1
    MOVE_DOWN = 2
    MOVE_LEFT = 3
    MOVE_RIGHT = 4

    START = 5
    RESTART = 6
    EXIT = 7