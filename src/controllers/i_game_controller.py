from abc import ABC, abstractmethod
from data.events import Event


class IGameController(ABC):
    @abstractmethod
    def handle_event(self, event: Event):
        pass
