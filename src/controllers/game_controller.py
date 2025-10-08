from controllers.i_game_controller import IGameController
from models.game_model import GameModel
from data.events import Event
from data.stages import Stage
from data.directions import Direction
import threading


class GameController(IGameController):
    def __init__(self, model: GameModel, tps: int):
        self.__model = model
        self.__tick_period = 1 / tps
        self.__last_essential_event = Event.PASS
        self.__is_running = True
        self.restart_timer()

    def restart_timer(self):
        self.__timer_tick = threading.Timer(
            interval=self.__tick_period, function=self.next_tick
        )
        self.__timer_tick.daemon = True
        self.__timer_tick.start()

    def next_tick(self):
        self.restart_timer()

        if self.__last_essential_event == Event.MOVE_UP:
            self.__model.set_direction(Direction.UP)
        if self.__last_essential_event == Event.MOVE_DOWN:
            self.__model.set_direction(Direction.DOWN)
        if self.__last_essential_event == Event.MOVE_LEFT:
            self.__model.set_direction(Direction.LEFT)
        if self.__last_essential_event == Event.MOVE_RIGHT:
            self.__model.set_direction(Direction.RIGHT)

        if self.__last_essential_event == Event.PAUSE:
            return

        if self.__last_essential_event == Event.TO_GAME:
            self.__model.set_stage(Stage.GAME)
            self.__last_essential_event = Event.PAUSE
            return
        if self.__last_essential_event == Event.TO_START_MENU:
            self.__model.set_stage(Stage.START_MENU)

        self.__model.go_straight()
        # set to default after processing
        self.__last_essential_event = Event.PASS

    def handle_event(self, event: Event):
        if event == Event.EVENTS_NUM:
            print("ERROR (GameController): wrong event")
            return

        if event != Event.PASS:
            self.__last_essential_event = event
