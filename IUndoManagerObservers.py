from abc import ABC, abstractmethod
 
class UndoStackStatusObserver(ABC):
    def __init__(self) -> None:
        super().__init__()
        
    @abstractmethod
    def updateUndoStackStatus(self, isNotEmpty: bool):
        pass
    
class RedoStackStatusObserver(ABC):
    def __init__(self) -> None:
        super().__init__()
        
    @abstractmethod
    def updateRedoStackStatus(self, isNotEmpty: bool):
        pass
