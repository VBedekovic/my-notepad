from abc import ABC, abstractmethod

class ClipboardObserver(ABC):
    def __init__(self):
        super().__init__()
    
    @abstractmethod
    def updateClipboard(self, isNotEmpty: bool):
        pass
    