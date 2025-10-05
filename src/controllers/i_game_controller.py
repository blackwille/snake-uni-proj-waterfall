from abc import ABC, abstractmethod
from data_classes.events import Event


class IGameController(ABC):
    @abstractmethod
    def handle_event(self, event: "Event"):
        pass
