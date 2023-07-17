from abc import ABC, abstractmethod

class TextObserver(ABC):
    def __init__(self):
        super().__init__()
    
    @abstractmethod
    def updateText(self, lines: list[str]):
        pass
    