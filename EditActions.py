from IEditAction import *
from IModelReciver import *
from LocationObjects import *

class DeleteBeforeAction(EditAction):
    def __init__(self, model: TextEditorModelReciver, char: str, location: Location):
        super().__init__() 
        self.modelReciver = model
        self.deletedChar = char
        self.location = location
        
    def execute_undo(self):
        self.modelReciver.cursorJump(self.location.copy())
        self.modelReciver.insert(self.deletedChar)
        
    def execute_do(self):
        self.modelReciver.cursorJump(self.location.copy())
        self.modelReciver.deleteAfter()

class DeleteAfterAction(EditAction):
    def __init__(self, model: TextEditorModelReciver, char: str, location: Location):
        super().__init__() 
        self.modelReciver = model
        self.deletedChar = char
        self.location = location
        
    def execute_undo(self):
        self.modelReciver.cursorJump(self.location.copy())
        self.modelReciver.insert(self.deletedChar)
        self.modelReciver.cursorJump(self.location.copy())
        
    def execute_do(self):
        self.modelReciver.cursorJump(self.location.copy())
        self.modelReciver.deleteAfter()

class DeleteRangeAction(EditAction):
    def __init__(self, model: TextEditorModelReciver, text: str, location: Location, locationRange: LocationRange):
        super().__init__() 
        self.modelReciver = model
        self.deletedText = text
        self.location = location
        self.locationRange = locationRange
        
    def execute_undo(self):
        self.modelReciver.cursorJump(self.location.copy())
        self.modelReciver.insertText(self.deletedText)
        
    def execute_do(self):
        self.modelReciver.deleteRange(self.locationRange)

class InsertAction(EditAction):
    def __init__(self, model: TextEditorModelReciver, char: str, location: Location):
        super().__init__() 
        self.modelReciver = model
        self.insertedChar = char
        self.location = location
        
    def execute_undo(self):
        self.modelReciver.cursorJump(self.location.copy())
        self.modelReciver.deleteAfter()
        
    def execute_do(self):
        self.modelReciver.cursorJump(self.location.copy())
        self.modelReciver.insert(self.insertedChar)
        
class InsertTextAction(EditAction):
    def __init__(self, model: TextEditorModelReciver, char: str, location: Location, locationRange: LocationRange):
        super().__init__() 
        self.modelReciver = model
        self.insertedText = char
        self.location = location
        self.locationRange = locationRange
        
    def execute_undo(self):
        self.modelReciver.deleteRange(self.locationRange)
        
    def execute_do(self):
        self.modelReciver.cursorJump(self.location.copy())
        self.modelReciver.insertText(self.insertedText)
