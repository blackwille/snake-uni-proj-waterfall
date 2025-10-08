from enum import Enum


class Event(Enum):
    PASS = 0
    MOVE_UP = 1
    MOVE_DOWN = 2
    MOVE_LEFT = 3
    MOVE_RIGHT = 4

    PAUSE = 5
    TO_START_MENU = 6
    TO_GAME = 7

    EVENTS_NUM = 8
