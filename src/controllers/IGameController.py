from abc import ABC, abstractmethod
from src.data_classes.EnumControllerEvents import ControllerEvent


class IGameController(ABC):
    @abstractmethod
    def handle_event(self, event: "ControllerEvent"):
        pass