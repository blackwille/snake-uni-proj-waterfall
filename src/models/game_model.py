from typing import List
from data_classes.game_state import GameState, Coord, MAP_SIZE
from data_classes.events import Event 
from views.i_game_view import IGameView
import random


class GameModel:
    def __init__(self):
        self.__snake_chains: List[Coord] = [Coord(MAP_SIZE // 2, MAP_SIZE // 2)]
        self.__direction: Event = Event.MOVE_RIGHT
        self.__map_size = {"width": MAP_SIZE, "height": MAP_SIZE}
        self.__apple: Coord = self.generate_apple()
        self.__stage: Event = Event.START_MENU
        self.__consumers: List[IGameView] = []


    def add_consumer(self, game_view: IGameView):
        self.__consumers.append(game_view)


    def set_direction(self, direction: Event):
        opposite_directions = {
            Event.MOVE_UP: Event.MOVE_DOWN,
            Event.MOVE_DOWN: Event.MOVE_UP,
            Event.MOVE_LEFT: Event.MOVE_RIGHT,
            Event.MOVE_RIGHT: Event.MOVE_LEFT
        }
        
        if direction != opposite_directions.get(self.__direction):
            self.__direction = direction


    def go_straight(self):
        if self.__stage != Event.RUNNING:
            return
        
        head = self.__snake_chains[0]

        if self.__direction == Event.MOVE_UP:
            new_head = Coord(head.x, head.y - 1)
        elif self.__direction == Event.MOVE_DOWN:
            new_head = Coord(head.x, head.y + 1)
        elif self.__direction == Event.MOVE_LEFT:
            new_head = Coord(head.x - 1, head.y)
        elif self.__direction == Event.MOVE_RIGHT:
            new_head = Coord(head.x + 1, head.y)
        else:
            return


        if (new_head.x < 0 or new_head.x >= self.__map_size["width"] or 
            new_head.y < 0 or new_head.y >= self.__map_size["height"]):
            self.__stage = Event.GAME_OVER
            self.update_consumers()
            return

        if new_head in self.__snake_chains:
            self.__stage = Event.GAME_OVER
            self.update_consumers()
            return


        self.__snake_chains.insert(0, new_head)

        if new_head.x == self.__apple.x and new_head.y == self.__apple.y:
            self.__apple = self.generate_apple()
        else:
            self.__snake_chains.pop()

        self.update_consumers()


    def start(self):
        self.__stage = Event.RUNNING
        self.update_consumers()


    def update_consumers(self):
        game_state = GameState(
            snake=self.__snake_chains.copy(),
            apple=self.__apple,
            map_size=(self.__map_size["width"], self.__map_size["height"]),
            stage=self.__stage
        )
        for consumer in self.__consumers:
            consumer.update(game_state)

    def generate_apple(self) -> Coord:
        
        while True:
            apple = Coord(
                random.randint(0, self.__map_size["width"] - 1),
                random.randint(0, self.__map_size["height"] - 1)
            )
            if apple not in self.__snake_chains:
                return apple
