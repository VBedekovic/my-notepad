from tkinter import *
from TextEditor import TextEditor
from MyUI import *
from MyPluginFactory import loadPlugins

root = Tk()
root.title("My notepad--")

editor = TextEditor(root, loadPlugins())
menu = MyMenu(root, editor)
toolbar = MyToolbar(root, editor)
statusbar = MyStatusBar(root, editor)

root.geometry("800x600+100+100")
root.config(menu=menu)
toolbar.pack(side=TOP, fill=X)
editor.pack(fill=BOTH, expand=1)
statusbar.pack(side=BOTTOM, fill=X)
root.mainloop()
        