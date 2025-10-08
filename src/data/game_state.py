from dataclasses import dataclass, field
from data.stages import Stage
from data.coord import Coord

DEFAULT_MAP_SIZE = 31


@dataclass
class GameState:
    stage: Stage = Stage.START_MENU
    map_size: tuple[int, int] = (DEFAULT_MAP_SIZE, DEFAULT_MAP_SIZE)
    snake: list[Coord] = field(
        default_factory=lambda: [Coord(DEFAULT_MAP_SIZE // 2, DEFAULT_MAP_SIZE // 2)]
    )
    apple: Coord = field(default_factory=lambda: Coord(0, 0))
