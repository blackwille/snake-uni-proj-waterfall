from data.game_state import GameState, Coord
from data.stages import Stage
from data.directions import Direction
from views.i_game_view import IGameView
from configs.game_config import GameConfig
from random import randint
import threading


class GameModel:
    def __init__(self, lock: threading.Lock) -> None:
        game_config = GameConfig()

        self.__map_size = {
            "width": game_config.map_size[0],
            "height": game_config.map_size[1],
        }
        self.__snake_chains: list[Coord] = [
            Coord(self.__map_size["width"] // 2, self.__map_size["height"] // 2)
        ]
        self.__lock: threading.Lock = lock
        self.__direction: Direction | None = None
        self.__apple: Coord = self.__generate_apple()
        self.__stage: Stage = Stage.START_MENU
        self.__consumers: list[IGameView] = []

    def add_consumer(self, game_view: IGameView) -> None:
        self.__consumers.append(game_view)

    def set_direction(self, direction: Direction) -> None:
        opposite_directions = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
        }

        if self.__direction is not None:
            if direction == opposite_directions.get(self.__direction):
                return

        self.__direction = direction

    def go_straight(self):
        if self.__stage != Stage.GAME:
            return

        head = self.__snake_chains[0]
        new_head = Coord(-1, -1)
        if self.__direction == Direction.UP:
            new_head = Coord(head.x, head.y - 1)
        elif self.__direction == Direction.DOWN:
            new_head = Coord(head.x, head.y + 1)
        elif self.__direction == Direction.LEFT:
            new_head = Coord(head.x - 1, head.y)
        elif self.__direction == Direction.RIGHT:
            new_head = Coord(head.x + 1, head.y)
        else:
            return

        if (
            new_head.x < 0
            or new_head.x >= self.__map_size["width"]
            or new_head.y < 0
            or new_head.y >= self.__map_size["height"]
        ):
            self.__stage = Stage.FAIL
            self.__update_consumers()
            return

        self.__snake_chains.insert(0, new_head)
        if new_head == self.__apple:
            self.__apple = self.__generate_apple()
        else:
            self.__snake_chains.pop()

        for chain in self.__snake_chains[1::]:
            if chain == new_head:
                self.__stage = Stage.FAIL
                self.__update_consumers()
                return

        self.__update_consumers()

    def set_stage(self, stage: Stage) -> None:
        if stage == Stage.START_MENU:
            self.__snake_chains: list[Coord] = [
                Coord(self.__map_size["width"] // 2, self.__map_size["height"] // 2)
            ]
            self.__direction = None
            self.__apple = self.__generate_apple()
        self.__stage = stage
        self.__update_consumers()

    def __update_consumers(self) -> None:
        game_state = GameState(
            snake=self.__snake_chains.copy(),
            apple=Coord(self.__apple.x, self.__apple.y),
            map_size=(self.__map_size["width"], self.__map_size["height"]),
            stage=self.__stage,
        )
        for consumer in self.__consumers:
            with self.__lock:
                consumer.update(game_state)

    def __generate_apple(self) -> Coord:
        possible_coords = []
        for i in range(self.__map_size["width"]):
            for j in range(self.__map_size["height"]):
                coord = Coord(x=i, y=j)
                if coord not in self.__snake_chains:
                    possible_coords.append(coord)

        apple_coord = Coord(0, 0)
        if len(possible_coords) > 0:
            apple_index = randint(0, len(possible_coords))
            apple_coord = possible_coords[apple_index]

        return apple_coord
