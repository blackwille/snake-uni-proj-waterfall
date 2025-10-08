from controllers.i_game_controller import IGameController
from models.game_model import GameModel
from data.events import Event
from data.stages import Stage
from data.directions import Direction
import threading
import time


class GameController(IGameController):
    def __init__(self, model: GameModel, tps: int):
        self.__model = model
        self.__tick_time = 1 / tps
        thread = threading.Thread(target=self.model_go_straight)
        thread.daemon = True
        thread.start()
        
    def model_go_straight(self):
        while True:
            self.__model.go_straight()
            time.sleep(self.__tick_time)

    def handle_event(self, event: Event):
        if event == Event.EVENTS_NUM:
            print("ERROR (GameController): wrong event")
            return

        if event == Event.MOVE_UP:
            self.__model.set_direction(Direction.UP)
        if event == Event.MOVE_DOWN:
            self.__model.set_direction(Direction.DOWN)
        if event == Event.MOVE_LEFT:
            self.__model.set_direction(Direction.LEFT)
        if event == Event.MOVE_RIGHT:
            self.__model.set_direction(Direction.RIGHT)

        if event == Event.TO_GAME:
            self.__model.set_stage(Stage.GAME)
        if event == Event.TO_START_MENU:
            self.__model.set_stage(Stage.START_MENU)

        print(event.name)
