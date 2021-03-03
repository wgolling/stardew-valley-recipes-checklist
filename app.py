"""Main app file."""

from pathlib import Path
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

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

    ## Notebook
    ntb_parent = ttk.Notebook(window)
    tab_cooking     = ttk.Frame(ntb_parent)
    tab_crafting    = ttk.Frame(ntb_parent)
    ntb_parent.add(tab_cooking, text="Cooking")
    ntb_parent.add(tab_crafting, text="Crafting")

    ## Checklists
    frm_cooking = ChecklistFrame(tab_cooking, cook)
    frm_crafting = ChecklistFrame(tab_crafting, crft)

    ## Pack widgets
    frm_cooking.pack()
    frm_crafting.pack()
    ntb_parent.pack(expand=1, fill="both")    
    
    # Menu bar

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
        save_data = {
            "cooking":  dict.fromkeys(cook.completed, True),                 # Can't write a set to json, so need to convert to dict.
            "crafting": dict.fromkeys(crft.completed, True)
        }
        save_json(filename, save_data)

    ## Menu definition
    menubar = tk.Menu(window)
    mnu_file = tk.Menu(menubar, tearoff=0)
    mnu_file.add_command(label="New", command=new)
    mnu_file.add_command(label="Open", command=load)
    mnu_file.add_command(label="Save", command=save)
    mnu_file.add_separator()
    mnu_file.add_command(label="Exit", command=window.quit)    
    menubar.add_cascade(label="File", menu=mnu_file)

    window.config(menu=menubar)
    window.mainloop()
