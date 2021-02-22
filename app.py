"""Main app file."""

from pathlib import Path
import tkinter as tk
from tkinter import filedialog

from obj.checklist import Checklist
from obj.widgets import ChecklistFrame
from lib.util import dict_to_string, load_json, save_json

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

    ## Display
    frm_cooking = ChecklistFrame(window, cook)
    frm_cooking.grid(row=0, column=0)

    frm_crafting = ChecklistFrame(window, crft, row=1)
    frm_crafting.grid(row=1, column=0)

    ## Menu helper functions
    def new():
        frm_cooking.set_completed(set())
        frm_crafting.set_completed(set())

    def load():
        filename = filedialog.askopenfilename(
                initialdir = Path(".") / "saves",
                title = "Select file",
                filetypes = (("checklist files","*.chk"),("all files","*.*"))
        )        
        load_data = load_json(filename)
        frm_cooking.set_completed(set(load_data["cooking"].keys()))
        frm_crafting.set_completed(set(load_data["crafting"].keys()))

    def save():
        filename = filedialog.asksaveasfilename(
                initialdir = Path(".") / "saves",
                title = "Select file",
                filetypes = (("checklist files","*.chk"),("all files","*.*"))
        )

        def set_to_dict(data):
            return {key:1 for key in data}

        save_data = {
            "cooking":  set_to_dict(cook.completed),
            "crafting": set_to_dict(crft.completed)
        }
        save_json(filename, save_data)
        print(filename)

    ## Menu bar

    menubar = tk.Menu(window)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="New", command=new)
    filemenu.add_command(label="Open", command=load)
    filemenu.add_command(label="Save", command=save)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=window.quit)    
    menubar.add_cascade(label="File", menu=filemenu)

    window.config(menu=menubar)
    window.mainloop()
