from abc import ABC, abstractmethod

class EditAction(ABC):
    def __init__(self):
        super().__init__()
    
    @abstractmethod
    def execute_do(self):
        pass
    
    @abstractmethod
    def execute_undo(self):
        pass
