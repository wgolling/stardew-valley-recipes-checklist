"""Main app file."""

import json
from pathlib import Path
import tkinter as tk
# from tkinter import ttk

from obj.checklist import Checklist
from lib.util import dict_to_string

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

def load_json(file_path):
    data = None
    with open(file_path) as f:
        data = json.load(f)
    return data

# Implements Brian Oakley's answer to the following StackOverflow question:
# https://stackoverflow.com/questions/3085696/adding-a-scrollbar-to-a-group-of-widgets-in-tkinter
class ScrollFrame(tk.Frame):
    def __init__(self, parent, content):

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")
        self.frame = tk.Frame(self.canvas, background="#ffffff")
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window(
            (4, 4),
            window=self.frame,
            anchor="nw",
            tags="self.frame"
        )

        self.frame.bind("<Configure>", self.onFrameConfigure)

        self.populate(content)

    def populate(self, content):
        cooking_recipes = tk.Label(
            master=self.frame,
            text=content, 
            fg="white",
            bg="#34A2FE"
        )
        cooking_recipes.pack()

    def onFrameConfigure(self, event):
        """Reset the scroll region to encompass the inner frame."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
