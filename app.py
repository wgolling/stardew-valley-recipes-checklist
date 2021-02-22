"""Main app file."""

from pathlib import Path
import tkinter as tk
from tkinter import filedialog

from obj.checklist import Checklist
from obj.widgets import ChecklistFrame
from lib.util import dict_to_string, load_json

def run():
    data_path = Path(".") / "data"
    cook = Checklist(load_json(data_path / "cooking_recipes.json"))
    crft = Checklist(load_json(data_path / "crafting_recipes.json"))
    app_window([cook, crft])

def app_window(checklists):
    window = tk.Tk()
    cook = checklists[0]
    crft = checklists[1]
    
    # Frames
    def do_nothing():
        print("Blah")

    def load():
        filename = filedialog.askopenfilename(
                initialdir = Path(".") / "saves",
                title = "Select file",
                filetypes = (("checklist files","*.chk"),("all files","*.*"))
        )        
        print(filename)

    menubar = tk.Menu(window)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="New", command=do_nothing)
    filemenu.add_command(label="Open", command=load)
    filemenu.add_command(label="Save", command=do_nothing)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=window.quit)    
    menubar.add_cascade(label="File", menu=filemenu)

    frm_cooking = ChecklistFrame(window, cook)
    frm_cooking.grid(row=0, column=0)

    frm_crafting = ChecklistFrame(window, crft, row=1)
    frm_crafting.grid(row=1, column=0)

    window.config(menu=menubar)
    window.mainloop()
