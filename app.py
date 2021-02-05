"""Main app file."""

import json
from pathlib import Path
import tkinter as tk

from obj.checklist import Checklist

def run():
    data_path = Path(".") / "data"
    cook = Checklist(load_json(data_path / "cooking_recipes.json"))
    crft = Checklist(load_json(data_path / "crafting_recipes.json"))
    app_window([cook, crft])

def app_window(checklists):
    window = tk.Tk()
    cook, crft = checklists[0], checklists[1]
    cook.print_recipes()
    cook.print_ingredients()
    crft.print_recipes()
    crft.print_ingredients()
    
    # Label
    greeting = tk.Label(
        text="Hello!", 
        fg="white",
        bg="#34A2FE",
        width=10,
        height=10
    )
    greeting.pack()

    window.mainloop()

def load_json(file_path):
    data = None
    with open(file_path) as f:
        data = json.load(f)
    return data
