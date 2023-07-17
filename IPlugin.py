from abc import ABC, abstractmethod
from TextEditorModel import TextEditorModel
from UndoManager import UndoManager
from Clipboard import ClipboardStack

class Plugin(ABC):
    def __init__(self) -> None:
        super().__init__()
    
    @abstractmethod
    def getName(self):
        pass
    
    @abstractmethod
    def getDescription(self):
        pass
    
    @abstractmethod
    def execute(self, model: TextEditorModel, undoManager: UndoManager, clipboardStack: ClipboardStack):
        pass
