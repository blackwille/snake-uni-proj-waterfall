from typing import List
from data.game_state import GameState, Coord, DEFAULT_MAP_SIZE
from data.stages import Stage
from data.directions import Direction
from views.i_game_view import IGameView
from random import randint


class GameModel:
    def __init__(self) -> None:
        self.__snake_chains: List[Coord] = [
            Coord(DEFAULT_MAP_SIZE // 2, DEFAULT_MAP_SIZE // 2)
        ]
        self.__direction: Direction = Direction.UP
        self.__map_size = {"width": DEFAULT_MAP_SIZE, "height": DEFAULT_MAP_SIZE}
        self.__apple: Coord = self.generate_apple()
        self.__stage: Stage = Stage.START_MENU
        self.__consumers: List[IGameView] = []

    def add_consumer(self, game_view: IGameView):
        self.__consumers.append(game_view)

    def set_direction(self, direction: Direction):
        opposite_directions = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
        }

        if direction != opposite_directions.get(self.__direction):
            self.__direction = direction

    def go_straight(self):
        if self.__stage != Stage.GAME:
            return

        head = self.__snake_chains[0]

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
            self.update_consumers()
            return

        if new_head in self.__snake_chains:
            self.__stage = Stage.FAIL
            self.update_consumers()
            return

        self.__snake_chains.insert(0, new_head)

        if new_head.x == self.__apple.x and new_head.y == self.__apple.y:
            self.__apple = self.generate_apple()
        else:
            self.__snake_chains.pop()

        self.update_consumers()

    def set_stage(self, stage: Stage):
        if stage == Stage.START_MENU:
            self.__snake_chains: List[Coord] = [
                Coord(DEFAULT_MAP_SIZE // 2, DEFAULT_MAP_SIZE // 2)
            ]
        self.__stage = stage
        self.update_consumers()

    def update_consumers(self):
        game_state = GameState(
            snake=self.__snake_chains.copy(),
            apple=self.__apple,
            map_size=(self.__map_size["width"], self.__map_size["height"]),
            stage=self.__stage,
        )
        for consumer in self.__consumers:
            consumer.update(game_state)

    def generate_apple(self) -> Coord:
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
