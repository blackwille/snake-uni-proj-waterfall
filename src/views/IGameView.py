from abc import ABC, abstractmethod
from src.controllers import IGameController
from src.data_classes import GameState


class IGameView(ABC):
    @abstractmethod
    def handle_event(self):
        pass

    @abstractmethod
    def set_controller(self, controller: "IGameController"):
        pass

    @abstractmethod
    def show(self):
        pass

    @abstractmethod
    def set_controller(self, state: "GameState"):
        pass