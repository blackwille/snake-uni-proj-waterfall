from abc import ABC, abstractmethod
from controllers.i_game_controller import IGameController
from data.game_state import GameState


class IGameView(ABC):
    @abstractmethod
    def watch_events(self) -> None:
        pass

    @abstractmethod
    def set_controller(self, controller: IGameController) -> None:
        pass

    @abstractmethod
    def show(self) -> bool:
        pass

    @abstractmethod
    def update(self, state: GameState) -> None:
        pass
