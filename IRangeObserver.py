from abc import ABC, abstractmethod

class RangeObserver(ABC):
    def __init__(self) -> None:
        super().__init__()
    
    @abstractmethod
    def updateRange(self, isActive: bool):
        pass
