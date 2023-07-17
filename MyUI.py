from tkinter import *
from IUndoManagerObservers import *
from IRangeObserver import *
from IClipboardObserver import *
from ICursorObserver import *
from ITextObserver import *
from LocationObjects import *
from TextEditor import TextEditor
from UndoManager import UndoManager

class MyMenu(Menu, UndoStackStatusObserver, RedoStackStatusObserver, ClipboardObserver, RangeObserver):
    def __init__(self, root, editor: TextEditor):
        super().__init__(root)
        
        undoManager = UndoManager.getInstance()
        undoManager.attachUndoStackStatusObserver(self)
        undoManager.attachRedoStackStatusObserver(self)
        editor.clipboard.attachClipboardObserver(self)
        editor.attachRangeObserver(self)
        
        self.fileMenu = Menu(self, tearoff=0)
        self.fileMenu.add_command(label="Open", command=editor.openTextDocument)
        self.fileMenu.add_command(label="Save", command=editor.saveTextDocument)
        self.fileMenu.add_command(label="Exit", command=self.master.destroy)
        self.add_cascade(label="File", menu=self.fileMenu)

        self.editMenu = Menu(self, tearoff=0)
        self.editMenu.add_command(label="Undo", command=editor.undoLastAction)
        self.editMenu.add_command(label="Redo", command=editor.redoUndoneAction)
        self.editMenu.add_command(label="Cut", command=editor.cutText)
        self.editMenu.add_command(label="Copy", command=editor.copyText)
        self.editMenu.add_command(label="Paste", command=editor.pasteText)
        self.editMenu.add_command(label="Paste and Take", command=editor.popAndPasteText)
        self.editMenu.add_command(label="Delete selection", command=lambda:[editor.model.deleteAfter(),
                                                                       editor.highlightActionDelete()])
        self.editMenu.add_command(label="Clear document", command=editor.clearDoc)
        self.add_cascade(label="Edit", menu=self.editMenu)
        for i in range(0, 7):
            self.editMenu.entryconfig(i, state=DISABLED)

        self.moveMenu = Menu(self, tearoff=0)
        self.moveMenu.add_command(label="Cursor to document start", command=editor.jumpStart)
        self.moveMenu.add_command(label="Cursor to document end", command=editor.jumpEnd)
        self.add_cascade(label="Move", menu=self.moveMenu)
        
        
        if len(editor.plugins) > 0:
            self.pluginMenu = Menu(self, tearoff=0)
            for plugin in editor.plugins:
                execute = lambda boundp = plugin: boundp.execute(editor.model, undoManager, editor.clipboard)
                self.pluginMenu.add_command(label=plugin.getName(),
                                            command=execute)
            self.add_cascade(label="Plugins", menu=self.pluginMenu)
        

    def updateUndoStackStatus(self, isNotEmpty: bool):
        if isNotEmpty:
            self.editMenu.entryconfig(0, state=NORMAL)
        else:
            self.editMenu.entryconfig(0, state=DISABLED)
        
    def updateRedoStackStatus(self, isNotEmpty: bool):
        if isNotEmpty:
            self.editMenu.entryconfig(1, state=NORMAL)
        else:
            self.editMenu.entryconfig(1, state=DISABLED)
    
    def updateClipboard(self, isNotEmpty: bool):
        if isNotEmpty:
            self.editMenu.entryconfig(4, state=NORMAL)
            self.editMenu.entryconfig(5, state=NORMAL)
        else:
            self.editMenu.entryconfig(4, state=DISABLED)
            self.editMenu.entryconfig(5, state=DISABLED)
            
    def updateRange(self, isActive: bool):
        if isActive:
            self.editMenu.entryconfig(2, state=NORMAL)
            self.editMenu.entryconfig(3, state=NORMAL)
            self.editMenu.entryconfig(6, state=NORMAL)
        else:
            self.editMenu.entryconfig(2, state=DISABLED)
            self.editMenu.entryconfig(3, state=DISABLED)
            self.editMenu.entryconfig(6, state=DISABLED)
            

class MyToolbar(Frame, UndoStackStatusObserver, RedoStackStatusObserver, ClipboardObserver, RangeObserver):
    def __init__(self, root, editor: TextEditor):
        super().__init__(root, bg="dark grey")
        
        undoManager = UndoManager.getInstance()
        undoManager.attachUndoStackStatusObserver(self)
        undoManager.attachRedoStackStatusObserver(self)
        editor.clipboard.attachClipboardObserver(self)
        editor.attachRangeObserver(self)
        
        self.undoButton = Button(self, text="Undo", command=editor.undoLastAction)
        self.undoButton.pack(side=LEFT, padx=2, pady=2)
        self.redoButton = Button(self, text="Redo", command=editor.redoUndoneAction)
        self.redoButton.pack(side=LEFT, padx=2, pady=2)
        self.cutButton = Button(self, text="Cut", command=editor.cutText)
        self.cutButton.pack(side=LEFT, padx=2, pady=2)
        self.copyButton = Button(self, text="Copy", command=editor.copyText)
        self.copyButton.pack(side=LEFT, padx=2, pady=2)
        self.pasteButton = Button(self, text="Paste", command=editor.pasteText)
        self.pasteButton.pack(side=LEFT, padx=2, pady=2)
        
        self.undoButton["state"] = DISABLED
        self.redoButton["state"] = DISABLED
        self.cutButton["state"] = DISABLED
        self.copyButton["state"] = DISABLED
        self.pasteButton["state"] = DISABLED
        
    def updateUndoStackStatus(self, isNotEmpty: bool):
        if isNotEmpty:
            self.undoButton["state"] = NORMAL
        else:
            self.undoButton["state"] = DISABLED
        
    def updateRedoStackStatus(self, isNotEmpty: bool):
        if isNotEmpty:
            self.redoButton["state"] = NORMAL
        else:
            self.redoButton["state"] = DISABLED
    
    def updateClipboard(self, isNotEmpty: bool):
        if isNotEmpty:
            self.pasteButton["state"] = NORMAL
        else:
            self.pasteButton["state"] = DISABLED
            
    def updateRange(self, isActive: bool):
        if isActive:
            self.cutButton["state"] = NORMAL
            self.copyButton["state"] = NORMAL
        else:
            self.cutButton["state"] = DISABLED
            self.copyButton["state"] = DISABLED


class MyStatusBar(Label, CursorObserver, TextObserver):
    def __init__(self, root, editor: TextEditor):
        super().__init__(root, bd=1, relief=SUNKEN, anchor=E)
        
        self.editor = editor
        self.editor.model.attachCursorObserver(self)
        self.editor.model.attachTextObserver(self)
        
        self.lineLable = Label(self, text="Text line count: {}".format(len(self.editor.model.lines)),
                               bd=1, relief=SUNKEN, anchor=W, padx=10)
        self.cursorLable = Label(self, text="Ln 1, Col 1", bd=1, relief=SUNKEN, anchor=W, padx=15)

        self.lineLable.pack(side=RIGHT)
        self.cursorLable.pack(side=RIGHT)
        
    def updateCursorLocation(self, loc: Location):
        self.cursorLable["text"] = "Ln {}, Col {}".format(loc.line + 1, loc.column + 1)
    
    def updateText(self, lines: list[str]):
        self.lineLable["text"] = "Text line count: {}".format(len(lines))
