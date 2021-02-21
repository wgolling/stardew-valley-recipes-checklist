"""Custom widgets for the user interface."""

import tkinter as tk
from functools import partial
from lib.util import dict_to_string

class ChecklistFrame(tk.Frame):

    def __init__(self, parent, checklist, row=0):
        tk.Frame.__init__(self, parent)
        
        self.frm_recipes = RecipesFrame(self, checklist)
        self.frm_recipes.grid(row=row, column=0)
        self.frm_ingredients = IngredientsFrame(self, checklist)
        self.frm_ingredients.grid(row=row, column=1)

    def refresh_ingredients(self):
        self.frm_ingredients.refresh_ingredients()


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

        self.parent = parent
        self.populate(content)

    def populate(self, content):
        lbl_content = tk.Label(
            master=self.frame,
            text=content, 
            fg="white",
            bg="#34A2FE"
        )
        lbl_content.pack()

    def onFrameConfigure(self, event):
        """Reset the scroll region to encompass the inner frame."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


class RecipesFrame(ScrollFrame):

    def toggle(self, checklist, recipe):
        print(recipe)
        checklist.toggle_recipe(recipe)
        print(str(checklist.completed))
        self.parent.refresh_ingredients()

    def populate(self, checklist):
        for k in checklist.recipes.keys():
            name = str(k)
            toggle_recipe = partial(self.toggle, checklist, name)
            btn_recipe = tk.Button(master=self.frame, command=toggle_recipe, text=name)
            btn_recipe.pack()


class IngredientsFrame(ScrollFrame):

    def populate(self, checklist):
        self.checklist = checklist
        ingredients_string = dict_to_string(self.checklist.ingredients)
        self.lbl_ingredients = tk.Label(
            master=self.frame,
            text=ingredients_string, 
            fg="white",
            bg="#34A2FE"
        )
        self.lbl_ingredients.pack()

    def refresh_ingredients(self):
        ingredients_string = dict_to_string(self.checklist.ingredients)
        self.lbl_ingredients["text"] = ingredients_string
