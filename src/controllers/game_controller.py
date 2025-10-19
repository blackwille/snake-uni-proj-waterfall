import threading
from time import sleep

from controllers.i_game_controller import IGameController
from data.directions import Direction
from data.events import Event
from data.stages import Stage
from models.game_model import GameModel


class GameController(IGameController):
    def __init__(self, model: GameModel, tps: int) -> None:
        self.__model = model
        self.__tick_period = 1 / tps
        self.__last_essential_event = Event.PASS
        self.__ticker_thread = threading.Thread(target=self.__tick, daemon=True)
        self.__ticker_thread.start()

    def __tick(self) -> None:
        while True:
            self.__next_tick()
            sleep(self.__tick_period)

    def __next_tick(self) -> None:
        event_to_direction: dict = {
            Event.MOVE_UP: Direction.UP,
            Event.MOVE_DOWN: Direction.DOWN,
            Event.MOVE_LEFT: Direction.LEFT,
            Event.MOVE_RIGHT: Direction.RIGHT,
        }

        is_event_have_direction = (
            self.__last_essential_event in event_to_direction.keys()
        )
        if is_event_have_direction:
            self.__model.set_direction(event_to_direction[self.__last_essential_event])

        is_pass = self.__last_essential_event == Event.PASS
        if is_event_have_direction or is_pass:
            self.__model.go_straight()

        if self.__last_essential_event == Event.PAUSE:
            return
        if self.__last_essential_event == Event.TO_GAME:
            self.__model.set_stage(Stage.GAME)
            self.__last_essential_event = Event.PAUSE
            return
        if self.__last_essential_event == Event.TO_START_MENU:
            self.__model.set_stage(Stage.START_MENU)

        # set to default after processing
        self.__last_essential_event = Event.PASS

    def handle_event(self, event: Event) -> None:
        if event == Event.EVENTS_NUM:
            print("ERROR (GameController): wrong event")
            return

        if event != Event.PASS:
            self.__last_essential_event = event
