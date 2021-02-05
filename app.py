"""Main app file."""

from pathlib import Path
import tkinter as tk

from obj.checklist import Checklist
from obj.widgets import ScrollFrame
from lib.util import dict_to_string, load_json

def run():
    data_path = Path(".") / "data"
    cook = Checklist(load_json(data_path / "cooking_recipes.json"))
    crft = Checklist(load_json(data_path / "crafting_recipes.json"))
    app_window([cook, crft])

def app_window(checklists):
    window = tk.Tk()
    cook = checklists[0]
    # crft = checklists[1]
    cooking_recipes_string = dict_to_string(cook.recipes)
    cooking_ingredients_string = dict_to_string(cook.ingredients)
    # crafting_recipes_string = dict_to_string(crft.recipes)
    # crafting_ingredients_string = dict_to_string(crft.ingredients)
    
    # Frames
    cooking_recipes_frame = ScrollFrame(window, cooking_recipes_string)
    cooking_recipes_frame.grid(row=0, column=0, sticky="ns")
    cooking_ingredients_frame = ScrollFrame(window, cooking_ingredients_string)
    cooking_ingredients_frame.grid(row=0, column=1, sticky="ns")

    window.mainloop()
