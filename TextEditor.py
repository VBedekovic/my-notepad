import os
from tkinter import *
from ICursorObserver import *
from ITextObserver import *
from IPlugin import *
from IRangeObserver import *
from LocationObjects import *
from tkinter import filedialog

class TextEditor(Canvas, CursorObserver, TextObserver):
    def __init__(self, root: Tk, plugins: list[Plugin] = [], model: TextEditorModel = TextEditorModel()):
        super().__init__()
        
        self.plugins = plugins
        
        self.root = root
        self.openFile = False
        self.fileTitle = "Untitled"
        self.filePath = ""
        
        self.root.title(self.fileTitle + " - " + "My notepad--")

        self.activeRangeInput = False
        self.activeRange = False
        self.activeRangeObservers: list[RangeObserver] = []
        self.rangeInitLocation = Location(0, 0)
        
        self.clipboard = ClipboardStack()
        
        self.model = model
        self.model.attachCursorObserver(self)
        self.model.attachTextObserver(self)
        self.initComponent()
        

    def closeWindow(self, event):
        self.master.destroy()

    def initComponent(self):    
        i = 0
        for line in self.model.allLines():
            self.create_text(5, 8 + 16 * i, anchor=W, font="Consolas 12", text = line, tag=("line" + str(i), "lines"))
            i += 1
            
        self.create_line(5 + 0 * 9, 2 + 0 * 16, 5 + 0 * 9, 16 + 0 * 16, fill="red", tag="cursor")
        
        
        
        self.master.bind('<Escape>', self.closeWindow)
        
        self.master.bind('<Left>', self.model.moveCursorLeft)
        self.master.bind('<Right>', self.model.moveCursorRight)
        self.master.bind('<Up>', self.model.moveCursorUp)
        self.master.bind('<Down>', self.model.moveCursorDown)
        
        self.master.bind('<BackSpace>', self.model.deleteBefore)
        self.master.bind('<Delete>', self.model.deleteAfter)
        
        self.master.bind('<KeyPress-Shift_L>', self.startDrawHighlight)
        self.master.bind('<KeyRelease-Shift_L>', self.endDrawHighlight)
        
        self.master.bind('<Left>', self.drawHighlight, add="+")
        self.master.bind('<Right>', self.drawHighlight, add="+")
        self.master.bind('<Up>', self.drawHighlight, add="+")
        self.master.bind('<Down>', self.drawHighlight, add="+")
        
        self.master.bind('<BackSpace>', self.highlightActionDelete, add="+")
        self.master.bind('<Delete>', self.highlightActionDelete, add="+")
        
        self.master.bind('<Key>', self.keyInput)
        self.master.bind('<Delete>', self.highlightActionInsert, add="+")
        
        self.master.bind('<Control-c>', self.copyText)
        self.master.bind('<Control-x>', self.cutText)
        self.master.bind('<Control-v>', self.pasteText)
        self.master.bind('<Control-V>', self.popAndPasteText)
        
        self.master.bind('<Control-z>', self.undoLastAction)
        self.master.bind('<Control-y>', self.redoUndoneAction)
        
    def attachRangeObserver(self, observer: RangeObserver):
        self.activeRangeObservers.append(observer)
    
    def dettachRangeObserver(self, observer: RangeObserver):
        self.activeRangeObservers.remove(observer)
        
    def notifyRangeObservers(self):
        for ro in self.activeRangeObservers:
            ro.updateRange(self.activeRange)
   
    def updateCursorLocation(self, loc: Location):
        self.coords("cursor", 5 + loc.column * 9, 2 + loc.line * 16, 5 + loc.column * 9, 16 + loc.line * 16)
        
    def updateText(self, lines: list[str]):
        self.delete("lines")
        i = 0
        for line in lines:
            self.create_text(5, 8 + 16 * i, anchor=W, font="Consolas 12", text = line, tag=("line" + str(i), "lines"))
            i += 1
            
    def drawHighlight(self, event = None):
        selectionRange = self.model.getSelectionRange()
        if not self.activeRangeInput:
            selectionRange.start = self.model.cursorLocation.copy()
            selectionRange.end = self.model.cursorLocation.copy()
            self.activeRange = False
            self.notifyRangeObservers()
        

        else:
            if self.rangeInitLocation == selectionRange.start and self.model.cursorLocation > self.rangeInitLocation:
                selectionRange.end =  self.model.cursorLocation.copy()
            elif self.rangeInitLocation == selectionRange.start and self.model.cursorLocation < self.rangeInitLocation:
                selectionRange.start =  self.model.cursorLocation.copy()
                selectionRange.end =  self.rangeInitLocation.copy()
            elif self.rangeInitLocation == selectionRange.end and self.model.cursorLocation < self.rangeInitLocation:
                selectionRange.start =  self.model.cursorLocation.copy()
            elif self.rangeInitLocation == selectionRange.end and self.model.cursorLocation > self.rangeInitLocation:
                selectionRange.end =  self.model.cursorLocation.copy()
                selectionRange.start =  self.rangeInitLocation.copy()
            else:
                selectionRange.start = self.model.cursorLocation.copy()
                selectionRange.end =  self.model.cursorLocation.copy()
                
        self.model.setSelectionRange(selectionRange)
        
        self.delete("highlight")
        for i in range(selectionRange.start.line, selectionRange.end.line + 1):
            for j in range(selectionRange.start.column
                           if selectionRange.start.line == i
                           else 0, 
                           selectionRange.end.column 
                           if selectionRange.end.line == i 
                            else len(self.model.lines[i])):
                self.create_rectangle(5 + j * 9, 2 + i * 16, 5 + (j + 1) * 9, 16 + i * 16, width=0, fill="yellow", tag="highlight")
        self.tag_lower("highlight")
        
    def startDrawHighlight(self, event):
        self.activeRangeInput = True
        if not self.activeRange:
            self.rangeInitLocation = self.model.cursorLocation.copy()
            self.activeRange = True
            self.notifyRangeObservers()
    
    def endDrawHighlight(self, event):
        self.activeRangeInput = False
        
    def highlightActionDelete(self, event = None):
        self.activeRange = False
        self.notifyRangeObservers()
        self.drawHighlight(event)
        
    def highlightActionInsert(self, event = None):
        self.activeRangeInput = False
        self.drawHighlight(event)
        
    def keyInput(self, event):
        if event.keycode == 17: return
        self.model.insert(event.char)
        self.activeRangeInput = False
        self.drawHighlight(event)
        
    def textInput(self, event = None):
        self.model.insertText("Ovo je insertan text.\nOvaj red ima newline\nOvaj red nema newline")
        self.activeRangeInput = False
        self.drawHighlight(event)
        
    def copyText(self, event = None):
        text = self.model.getSelection()
        if text != None:
            self.clipboard.push(text)
            
    def cutText(self, event = None):
        text = self.model.getSelection()
        if text != None:
            self.clipboard.push(text)
            self.model.deleteAfter()
            self.highlightActionDelete(event)
        
    def pasteText(self, event = None):
        if not self.clipboard.isStackEmpty():
            self.model.insertText(self.clipboard.getStackPeek())
            self.highlightActionDelete(event)
        
    def popAndPasteText(self, event = None):
        if not self.clipboard.isStackEmpty():
            self.model.insertText(self.clipboard.pop())
            self.highlightActionInsert(event)
    
    def undoLastAction(self, event = None):
        UM_Instance = UndoManager.getInstance()
        UM_Instance.undo()
    
    def redoUndoneAction(self, event = None):
        UM_Instance = UndoManager.getInstance()
        UM_Instance.redo()
        
    def jumpStart(self, event = None):
        self.model.cursorJump(Location(0, 0))
        
    def jumpEnd(self, event = None):
        self.model.cursorJump(Location(len(self.model.lines) - 1,
                                            len(self.model.lines[-1])))
        
    def clearDoc(self, event = None):
        self.model.selectionRange = LocationRange(Location(0, 0), Location(0 ,0))
        self.activeRange = True
        self.model.deleteRange(LocationRange(Location(0, 0), 
                                                  Location(len(self.model.lines) - 1,
                                                           len(self.model.lines[-1]))))
        
        self.activeRangeInput = False
        self.drawHighlight()
    
    FILETYPES = [ ("My text file", ".mytxt"),
                 ("Text file", ".txt")]
    
    def openTextDocument(self, event = None):
        self.filePath = filedialog.askopenfilename(title='Open a mytxt file',
                                          initialdir='.\mySavedFiles',
                                          filetypes=TextEditor.FILETYPES)
        
        with open(self.filePath, "r") as file:
            rawText = file.read()
            self.fileTitle = os.path.basename(file.name).split(".")[0]
        
        self.clearDoc()
        self.model.insertText(rawText)
        self.jumpStart()
        
        self.clipboard.delete()
        UndoManager.getInstance().emptyAllStacks()
        
        self.openFile = True
        self.root.title(self.fileTitle + " - " + "My notepad--")
        
    
    def saveTextDocument(self, event = None):
        if not self.openFile:
            saveFile = filedialog.asksaveasfile(defaultextension=".mytxt",
                                            initialdir='.\mySavedFiles',
                                            filetypes=TextEditor.FILETYPES)
        else:
            saveFile = open(self.filePath, "w")
            
        rawText = "\n".join(self.model.lines)
        saveFile.write(rawText)
        saveFile.close()
