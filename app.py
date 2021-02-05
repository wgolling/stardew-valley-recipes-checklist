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
    frm_recipes = tk.Frame(master=window, relief=tk.SUNKEN, borderwidth=3)
    frm_recipes.grid(row=0, column=0, sticky="ns")
    frm_ingredients = tk.Frame(master=window, relief=tk.SUNKEN, borderwidth=3)
    frm_ingredients.grid(row=0, column=1, sticky="ns")

    # Frame contents
    cooking_recipes_frame = ScrollFrame(frm_recipes, cooking_recipes_string)
    cooking_recipes_frame.pack(side="top", fill="both", expand=True)
    cooking_ingredients_frame = ScrollFrame(frm_ingredients, cooking_ingredients_string)
    cooking_ingredients_frame.pack(side="top", fill="both", expand=True)

    # crafting_recipes = tk.Label(
    #     master=frm_recipes,
    #     text=crafting_recipes_string, 
    #     fg="white",
    #     bg="#34A2FE"
    # )
    # crafting_recipes.pack()
    # crafting_ingredients = tk.Label(
    #     master=frm_ingredients,
    #     text=crafting_ingredients_string, 
    #     fg="white",
    #     bg="#34A2FE"
    # )
    # crafting_ingredients.pack()

    window.mainloop()
