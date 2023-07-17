
from abc import ABC, abstractmethod
from LocationObjects import *

class TextEditorModelReciver(ABC):
    def __init__(self) -> None:
        super().__init__()
    
    @abstractmethod
    def deleteBefore(self, event = None):
        pass
    
    @abstractmethod      
    def deleteAfter(self, event = None):
        pass
    
    @abstractmethod
    def deleteRange(self, range: LocationRange):
        pass
    
    @abstractmethod
    def insert(self, c: str):
        pass
        
    @abstractmethod
    def insertText(self, text: str):
        pass
    
    @abstractmethod
    def cursorJump(self, loc: Location):
        pass
    