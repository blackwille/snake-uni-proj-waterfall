from dataclasses import dataclass, field
from data.stages import Stage
from data.coord import Coord


@dataclass
class GameState:
    stage: Stage = Stage.START_MENU
    map_size: tuple[int, int] = (0, 0)
    snake: list[Coord] = field(default_factory=lambda: [])
    apple: Coord = field(default_factory=lambda: Coord(0, 0))
