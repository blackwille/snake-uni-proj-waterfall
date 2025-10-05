from dataclasses import dataclass, field
from typing import List, Tuple
from data_classes.EnumEvent import Event

MAP_SIZE = 30


@dataclass
class Coord:
    x: int
    y: int


@dataclass
class GameState:
    snake: List[Coord] = field(default_factory=lambda: [Coord(MAP_SIZE // 2, MAP_SIZE // 2)])
    apple: Coord = field(default_factory=lambda: Coord(0, 0))
    map_size: Tuple[int, int] = (MAP_SIZE, MAP_SIZE)
    stage: Event = Event.START_MENU
