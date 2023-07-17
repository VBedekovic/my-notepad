from abc import ABC, abstractmethod
from LocationObjects import Location

class CursorObserver(ABC):
    def __init__(self):
        super().__init__()
    
    @abstractmethod
    def updateCursorLocation(self, loc: Location):
        pass