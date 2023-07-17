# Notepad Program with Design Patterns

This repository contains a notepad program implemented in Python, utilizing the tkinter library. The project was developed as an exercise to demonstrate the implementation of various design patterns.

## Key Features

- The program doesn't use built-in text frames or textarea frames; instead, it draws all the elements on a canvas object.
- The TextEditor component is responsible for managing the cursor's position, handling keyboard inputs, and displaying the text on the screen.
- All actions in the program can be performed either via keyboard shortcuts or through buttons provided in the user interface.
- The cursor can be moved using the arrow keys.
- You can save files as .mytxt and open them later. Two example files are in the mySavedFiles folder.

## Clipboard Functionality

The Clipboard component enables common text editor actions:

- **CTRL+C**: Copies the current selection (if any) to the clipboard stack.
- **CTRL+X**: Copies the current selection (if any) to the clipboard stack and then deletes it from the text model.
- **CTRL+V**: Retrieves text from the top of the clipboard stack and inserts it into the text model using the `insert(...)` method.
- **CTRL+SHIFT+V**: Retrieves text from the top of the clipboard stack, removes it from the stack, and inserts it into the text model using the `insert(...)` method.

## Undo and Redo Functionality

The UndoManager singleton manages the undo and redo stacks, providing the following methods:

- **CTRL+Z**: Removes the last command from the undo stack, adds it to the redo stack, and executes the `execute_undo()` method.
- **CTRL+Y**: Removes the last command from the redo stack, executes the `execute_do()` method, and switches the command to the undo stack.

## Plugin System

The program incorporates a plugin factory, which allows for dynamic addition of new features to the text editor. Plugins are defined by the `IPlugin` interface. Two example plugins are included:

1. **Statistics (Statistika) Plugin**: Counts the number of lines, words, and letters in a document and displays this information to the user in a dialog.
2. **Uppercase (VelikoSlovo) Plugin**: Modifies the document by capitalizing the first letter of each word.

## Getting Started
Ensure you have Python 3 installed.

To run the notepad program locally, follow these steps:

1. Clone this repository: `git clone https://github.com/vbedekovic/my-notepad.git`
2. Run the main Python file: `py myNotepadMain.py`




