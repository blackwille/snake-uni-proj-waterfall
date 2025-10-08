from views.game_view import GameView
from models.game_model import GameModel
from controllers.game_controller import GameController
import time
import threading


class GameApp:
    def __init__(self, fps: int, tps: int) -> None:
        lock_ = threading.Lock()
        self.__model = GameModel(lock=lock_)
        self.__controller = GameController(self.__model, tps)
        self.__view = GameView(lock=lock_)
        self.__view.set_controller(self.__controller)
        self.__model.add_consumer(self.__view)

        self.__frame_time = 1 / fps
        self.__frames_in_tick = fps // tps

    def run(self) -> None:
        frame_count = 0
        while self.__view.show():
            frame_count += 1
            self.__view.watch_events()
            time.sleep(self.__frame_time)

    def destroy(self) -> None:
        self.__view.destroy()
