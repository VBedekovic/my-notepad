from abc import ABC, abstractmethod
from tkinter import messagebox
import re
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


class Statistika(Plugin):
    def __init__(self):
        super().__init__()
        
        self.name = "Statistika"
        self.description = "Plugin koji broji koliko ima redaka, riječi i slova u dokumentu i to prikazuje korisniku u dijalogu."
        
    def getName(self):
        return self.name
    
    def getDescription(self):
        return self.description
    
    def execute(self, model: TextEditorModel, undoManager: UndoManager, clipboardStack: ClipboardStack):
        linesCount = len(model.lines)
        alphaCount = 0
        wordCount = 0
        for line in model.lines:
            alphaCount += sum(c.isalpha() for c in line)
            wordCount += len(re.findall(r'\w+', line))
        messagebox.showinfo(title="Statistika",
                            message="Broj redaka: {}\nBroj slova: {}\nBroj riječi: {}".format(linesCount, alphaCount, wordCount))
            
    
def construct():
    return Statistika()
