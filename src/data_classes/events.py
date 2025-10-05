from enum import Enum


class Event(Enum):
    MOVE_UP = 1
    MOVE_DOWN = 2
    MOVE_LEFT = 3
    MOVE_RIGHT = 4

    START_MENU = 5
    RUNNING = 6
    GAME_OVER = 7
