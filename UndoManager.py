from __future__ import annotations
from SingletonMetaclass import *
from IUndoManagerObservers import *
from IEditAction import *
    
class UndoManager(metaclass=Singleton):
    _instance: UndoManager = None
    
    def __init__(self) -> None:
        if UndoManager._instance != None:
            raise Exception("UndoManager is already instanced!")
        else:
            self.undoStack: list[EditAction] = []
            self.redoStack: list[EditAction] = []
            self.__actionCalledByUM = False
            
            self.undoStackObservers: list[UndoStackStatusObserver] = []
            self.redoStackObservers: list[RedoStackStatusObserver] = []
    
    @staticmethod  
    def getInstance():
        if UndoManager._instance == None:
            UndoManager._instance = UndoManager()
        return UndoManager._instance
        
    def undo(self):
        if len(self.undoStack) != 0:
            self.__actionCalledByUM = True
            action = self.undoStack.pop()
            self.redoStack.append(action)
            action.execute_undo()
            self.__actionCalledByUM = False
            self.notifyRedoStackStatusObservers()
            self.notifyUndoStackStatusObservers()
        
    def redo(self):
        if len(self.redoStack) != 0:
            self.__actionCalledByUM = True
            action = self.redoStack.pop()
            self.undoStack.append(action)
            action.execute_do()
            self.__actionCalledByUM = False
            self.notifyRedoStackStatusObservers()
            self.notifyUndoStackStatusObservers()
        
    def push(self, c: EditAction):
        self.redoStack = []
        self.undoStack.append(c)
        self.notifyRedoStackStatusObservers()
        self.notifyUndoStackStatusObservers()
        
    def snapshotAction(self, c: EditAction):
        if not self.__actionCalledByUM:
            self.push(c)

    def emptyAllStacks(self):
        self.undoStack = []
        self.redoStack = []
        self.notifyRedoStackStatusObservers()
        self.notifyUndoStackStatusObservers()
        
    def attachUndoStackStatusObserver(self, observer: UndoStackStatusObserver):
        self.undoStackObservers.append(observer)
        
    def attachRedoStackStatusObserver(self, observer: RedoStackStatusObserver):
        self.redoStackObservers.append(observer)
        
    def dettachUndoStackStatusObserver(self, observer: UndoStackStatusObserver):
        self.undoStackObservers.remove(observer)
        
    def dettachRedoStackStatusObserver(self, observer: RedoStackStatusObserver):
        self.redoStackObservers.remove(observer)
        
    def notifyUndoStackStatusObservers(self):
        for so in self.undoStackObservers:
            so.updateUndoStackStatus(False if len(self.undoStack) == 0 else True)
    
    def notifyRedoStackStatusObservers(self):
        for so in self.redoStackObservers:
            so.updateRedoStackStatus(False if len(self.redoStack) == 0 else True)
