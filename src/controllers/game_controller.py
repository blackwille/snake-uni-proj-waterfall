from controllers.i_game_controller import IGameController
from models.game_model import GameModel
from data.events import Event
from data.stages import Stage
from data.directions import Direction
import threading


class GameController(IGameController):
    def __init__(self, model: GameModel, tps: int) -> None:
        self.__model = model
        self.__tick_period = 1 / tps
        self.__last_essential_event = Event.PASS
        self.__restart_timer()

    def __restart_timer(self) -> None:
        self.__timer_tick = threading.Timer(
            interval=self.__tick_period, function=self.__next_tick
        )
        self.__timer_tick.daemon = True
        self.__timer_tick.start()

    def __next_tick(self) -> None:
        self.__restart_timer()

        is_up = self.__last_essential_event == Event.MOVE_UP
        if is_up:
            self.__model.set_direction(Direction.UP)
        is_down = self.__last_essential_event == Event.MOVE_DOWN
        if is_down:
            self.__model.set_direction(Direction.DOWN)
        is_left = self.__last_essential_event == Event.MOVE_LEFT
        if is_left:
            self.__model.set_direction(Direction.LEFT)
        is_right = self.__last_essential_event == Event.MOVE_RIGHT
        if is_right:
            self.__model.set_direction(Direction.RIGHT)

        is_pass = self.__last_essential_event == Event.PASS
        if is_up or is_down or is_left or is_right or is_pass:
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
