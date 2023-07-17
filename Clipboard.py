from IClipboardObserver import *

class ClipboardStack:
    def __init__(self) -> None:
        self.textStack: list[str] = []
        self.clipboardObservers: list[ClipboardObserver] = [] 
    
    def push(self, text: str):
        self.textStack.append(text)
        self.notifyClipboardObservers()
        
    def pop(self):
        stackTop = self.textStack.pop()
        self.notifyClipboardObservers()
        return stackTop
    
    def getStackPeek(self):
        return self.textStack[-1]
    
    def isStackEmpty(self):
        if len(self.textStack) == 0:
            return True
        else:
            return False
        
    def delete(self):
        self.textStack = []
        self.notifyClipboardObservers()
        
    def attachClipboardObserver(self, observer: ClipboardObserver):
        self.clipboardObservers.append(observer)
        
    def dettachClipboardObserver(self, observer: ClipboardObserver):
        self.clipboardObservers.remove(observer)
        
    def notifyClipboardObservers(self):
        for cbo in self.clipboardObservers:
            cbo.updateClipboard(not self.isStackEmpty())
