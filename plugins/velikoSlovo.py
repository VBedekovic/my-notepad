from abc import ABC, abstractmethod
from string import capwords
from tkinter.messagebox import showinfo
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
    def execute(self, model, undoManager, clipboardStack):
        pass


class VelikoSlovo(Plugin):
    def __init__(self):
        super().__init__()
        
        self.name = "Veliko Slovo"
        self.description = "Prolazi kroz dokument i svako prvo slovo riječi mijenja u veliko ('ovo je tekst' ==> 'Ovo Je Tekst')."
        
    def getName(self):
        return self.name
    
    def getDescription(self):
        return self.description
    
    def execute(self, model: TextEditorModel, undoManager: UndoManager, clipboardStack: ClipboardStack):
        for i in range(len(model.lines)):
            model.lines[i] = capwords(model.lines[i])
            
        model.notifyTextObservers()
    
def construct():
    return VelikoSlovo()
