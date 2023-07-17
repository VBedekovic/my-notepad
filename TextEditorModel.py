from IModelReciver import *
from ICursorObserver import *
from ITextObserver import *
from UndoManager import UndoManager
from EditActions import *

class TextEditorModel(TextEditorModelReciver):
    def __init__(self, textString: str = ""):
        self.cursorObservers: list[CursorObserver] = []
        self.textObservers: list[TextObserver] = []
        
        self.lines: list[str] = []
        
        for line in textString.split("\n"):
            self.lines.append(line.replace("\t", "    "))
            
        self.selectionRange: LocationRange = LocationRange(Location(0, 0), Location(0, 0))
        self.cursorLocation: Location  = Location(0, 0)
        
    class _LinesRangeIterator:
        def __init__(self, lines: list[str], index1: int, index2: int):
            self.lines = lines
            self.index = index1
            self.end = index2
            self.len = len(lines)
            
        def __iter__(self):
            return self
            
        def __next__(self):
            if (self.index < self.end and self.index < self.len):
                line =  self.lines[self.index]
                self.index += 1
                return line
            else:
                raise StopIteration
                
    def allLines(self):
        return iter(self.lines)
    
    def linesRange(self, index1: int, index2: int):
        return iter(self._LinesRangeIterator(self.lines, index1, index2))
    
    
    def attachCursorObserver(self, observer: CursorObserver):
        self.cursorObservers.append(observer)
    
    def dettachCursorObserver(self, observer: CursorObserver):
        self.cursorObservers.remove(observer)
    
    def notifyCursorObservers(self):
        for co in self.cursorObservers:
            co.updateCursorLocation(self.cursorLocation)
            
    def attachTextObserver(self, observer: TextObserver):
        self.textObservers.append(observer)
        
    def dettachTextObserver(self, observer: TextObserver):
        self.textObservers.remove(observer)
        
    def notifyTextObservers(self):
        for to in self.textObservers:
            to.updateText(self.lines)
        
    
    def moveCursorLeft(self, event = None):
        if self.cursorLocation.column > 0:
            self.cursorLocation.column -= 1
            self.notifyCursorObservers()
        elif self.cursorLocation.line > 0:
            self.cursorLocation.line -= 1
            self.cursorLocation.column = len(self.lines[self.cursorLocation.line])
            self.notifyCursorObservers()
    
    def moveCursorRight(self, event = None):
        if self.cursorLocation.column < len(self.lines[self.cursorLocation.line]):
            self.cursorLocation.column += 1
            self.notifyCursorObservers()
        elif self.cursorLocation.line < len(self.lines) - 1:
            self.cursorLocation.line += 1
            self.cursorLocation.column = 0
            self.notifyCursorObservers()
    
    def moveCursorUp(self, event = None):
        if self.cursorLocation.line > 0:
            self.cursorLocation.line -= 1
            if self.cursorLocation.column > len(self.lines[self.cursorLocation.line]):
                self.cursorLocation.column = len(self.lines[self.cursorLocation.line])
            self.notifyCursorObservers()
    
    def moveCursorDown(self, event = None):
        if self.cursorLocation.line < len(self.lines) - 1:
            self.cursorLocation.line += 1
            if self.cursorLocation.column > len(self.lines[self.cursorLocation.line]):
                self.cursorLocation.column = len(self.lines[self.cursorLocation.line])
            self.notifyCursorObservers()   
        
    def cursorJump(self, loc: Location):
        self.cursorLocation = loc
        self.notifyCursorObservers()
    
    def deleteBefore(self, event = None):
        if self.selectionRange.valid():
            self.deleteRange(self.selectionRange)
        
        else:
            charAtLocationSnapshot = ""
            if self.cursorLocation.column > 0:
                charAtLocationSnapshot = self.lines[self.cursorLocation.line][self.cursorLocation.column - 1]
                self.lines[self.cursorLocation.line] = \
                    self.lines[self.cursorLocation.line][0 : self.cursorLocation.column - 1 : ] + \
                    self.lines[self.cursorLocation.line][self.cursorLocation.column : : ]
                self.notifyTextObservers()
                self.moveCursorLeft()
            elif self.cursorLocation.line > 0:
                charAtLocationSnapshot = "\n"
                self.cursorLocation.column = len(self.lines[self.cursorLocation.line - 1])
                
                self.lines[self.cursorLocation.line - 1] = \
                    self.lines[self.cursorLocation.line - 1] + self.lines[self.cursorLocation.line]
                self.lines.pop(self.cursorLocation.line)
                self.notifyTextObservers()
                
                self.cursorLocation.line = self.cursorLocation.line - 1
                self.notifyCursorObservers()
            
            cursorLocationSnapshot = self.cursorLocation.copy() 
            undoManager = UndoManager.getInstance()
            undoManager.snapshotAction(DeleteBeforeAction(self, charAtLocationSnapshot, cursorLocationSnapshot))
            
    def deleteAfter(self, event = None):
        if self.selectionRange.valid():
            self.deleteRange(self.selectionRange)
        
        else:
            charAtLocationSnapshot = ""
            if self.cursorLocation.column < len(self.lines[self.cursorLocation.line]):
                charAtLocationSnapshot = self.lines[self.cursorLocation.line][self.cursorLocation.column]
                self.lines[self.cursorLocation.line] = \
                    self.lines[self.cursorLocation.line][0 : self.cursorLocation.column : ] + \
                    self.lines[self.cursorLocation.line][self.cursorLocation.column + 1 : : ]
                self.notifyTextObservers()   
            elif self.cursorLocation.line < len(self.lines) - 1:
                charAtLocationSnapshot = "\n"
                self.lines[self.cursorLocation.line] = \
                    self.lines[self.cursorLocation.line] + self.lines[self.cursorLocation.line + 1]
                self.lines.pop(self.cursorLocation.line + 1)
                self.notifyTextObservers()
            
            cursorLocationSnapshot = self.cursorLocation.copy() 
            undoManager = UndoManager.getInstance()
            undoManager.snapshotAction(DeleteAfterAction(self, charAtLocationSnapshot, cursorLocationSnapshot))
            
    def deleteRange(self, range: LocationRange):
        if not range.valid(): return

        textAtLocationSnapshot = ""
        if range.start.line == range.end.line:
            textAtLocationSnapshot = self.lines[range.start.line][range.start.column : range.end.column]
            
            self.lines[range.start.line] = self.lines[range.start.line][0 : range.start.column : ] + \
                self.lines[range.start.line][range.end.column : : ]
        else:
            textAtLocationSnapshot = self.lines[range.start.line][range.start.column : ] + "\n"
            for line in self.lines[range.start.line + 1 : range.end.line]:
                textAtLocationSnapshot += line + "\n"
            
            textAtLocationSnapshot += self.lines[range.end.line][ : range.end.column]

            
            self.lines[range.start.line] = \
                self.lines[range.start.line][0 : range.start.column : ] + \
                self.lines[range.end.line][range.end.column : : ]
                
            self.lines = self.lines[0 : range.start.line + 1 : ] + self.lines[range.end.line + 1 : : ]
             
        self.notifyTextObservers()
        self.cursorLocation = range.start.copy()
        self.notifyCursorObservers()
        
        undoManager = UndoManager.getInstance()
        undoManager.snapshotAction(DeleteRangeAction(self, textAtLocationSnapshot, range.start.copy(), range.copy()))

   
    def getSelectionRange(self):
        return self.selectionRange
    
    def setSelectionRange(self, range: LocationRange):
        self.selectionRange = range
        
    def getSelection(self):
        if not self.selectionRange.valid(): return
        
        selection = ""
        for i in range(self.selectionRange.start.line, self.selectionRange.end.line + 1):
            for j in range(self.selectionRange.start.column
                           if self.selectionRange.start.line == i
                           else 0, 
                           self.selectionRange.end.column 
                           if self.selectionRange.end.line == i 
                        else len(self.lines[i])):
                selection += self.lines[i][j]
            selection += "\n"

        selection = selection[:-1]
        return selection
    
    def insert(self, c: str):
        if self.selectionRange.valid():
            self.deleteRange(self.selectionRange)
        
        if c == "\r":
            c = "\n"
        
        self.lines[self.cursorLocation.line] = \
            self.lines[self.cursorLocation.line][: self.cursorLocation.column] + \
            c + \
            self.lines[self.cursorLocation.line][self.cursorLocation.column :]
        if c == "\n":
            oldLine, newLine = self.lines[self.cursorLocation.line].split("\n")
            self.lines[self.cursorLocation.line] = oldLine
            self.lines.insert(self.cursorLocation.line + 1, newLine)
        self.notifyTextObservers()
        
        cursorLocationSnapshot = self.cursorLocation.copy() 
        
        self.cursorLocation.column += 1
        if c == "\n":
            self.cursorLocation.line += 1
            self.cursorLocation.column = 0
        self.notifyCursorObservers()
        
        undoManager = UndoManager.getInstance()
        undoManager.snapshotAction(InsertAction(self, c, cursorLocationSnapshot))
        
    def insertText(self, text: str):
        if self.selectionRange.valid():
            self.deleteRange(self.selectionRange)
            
        text = text.replace("\r", "\n")
        lastLineOfNewTextLen = len(text.split("\n")[-1])
        beginingPartOfSlicedLineLen = len(self.lines[self.cursorLocation.line][: self.cursorLocation.column])
        self.lines[self.cursorLocation.line] = \
            self.lines[self.cursorLocation.line][: self.cursorLocation.column] + \
            text + \
            self.lines[self.cursorLocation.line][self.cursorLocation.column :]
        
        newLines = self.lines[self.cursorLocation.line].split("\n")
        i = 0
        for newLine in newLines:
            if i == 0:  
                self.lines[self.cursorLocation.line] = newLine
            else:
                self.lines.insert(self.cursorLocation.line + i, newLine)
            i += 1
        self.notifyTextObservers()
        
        cursorLocationSnapshot = self.cursorLocation.copy() 
        
        self.cursorLocation.line = self.cursorLocation.line + i - 1
        if len(newLines) < 2:
            self.cursorLocation.column = beginingPartOfSlicedLineLen + lastLineOfNewTextLen
        else:
            self.cursorLocation.column = lastLineOfNewTextLen
        self.notifyCursorObservers()
        
        undoManager = UndoManager.getInstance()
        undoManager.snapshotAction(InsertTextAction(self, text, cursorLocationSnapshot,
                                          LocationRange(cursorLocationSnapshot.copy(),
                                                        self.cursorLocation.copy())))
