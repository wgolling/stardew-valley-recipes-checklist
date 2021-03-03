"""Custom widgets for the user interface."""

import tkinter as tk
from functools import partial
from lib.util import dict_to_string

class ChecklistFrame(tk.Frame):
    """A frame having a RecipesFrame and an IngredientsFrame as children.

    Displays total ingredient requirements for a Checklist. Allows a user to
    click buttons corresponding to recipes, which toggles their "completed"
    state and refreshes displays.
    
    Attributes:
        frm_recipes (:obj: `RecipesFrame`): A frame containing buttons for 
            toggling recipes.
        frm_ingredients (:obj: `IngredientsFrame`): A frame displaying ingredients.
    
    """

    def __init__(self, parent, checklist, row=0):
        """Constructs a ChecklistFrame given a parent frame and a Checklist.

        Args:
            parent (:obj: `Frame`): The parent frame.
            checklist (:obj: `Checklist`): The data structure which the GUI manipulates.
            row (:obj: `int`, optional): The row that self occupies in its
                parent's grid.

        """
        tk.Frame.__init__(self, parent)
        self.checklist = checklist
        
        self.frm_recipes = RecipesFrame(self, checklist)
        self.frm_recipes.grid(row=row, column=0)
        self.frm_ingredients = IngredientsFrame(self, checklist)
        self.frm_ingredients.grid(row=row, column=1)

    def set_completed(self, completed_set):
        """Sets the completed attribute of self.checklist and refreshes display."""
        self.checklist.set_completed(completed_set)
        self.refresh_display()

    def refresh_display(self):
        """Refreshes both the recipe and ingredient displays."""
        self.frm_recipes.refresh_buttons()
        self.refresh_ingredients()

    def refresh_ingredients(self):
        """Tells the ingredients frame to refresh its display."""
        self.frm_ingredients.refresh_ingredients()


class ScrollFrame(tk.Frame):
    """
    A general frame with a scrollbar on the right, populated by content.

    Subclasses should override the populate method.

    Implements Brian Oakley's answer to the following StackOverflow question:
    https://stackoverflow.com/questions/3085696/adding-a-scrollbar-to-a-group-of-widgets-in-tkinter

    """

    def __init__(self, parent, content):
        """Constructs a ScrollFrame given a parent frame and general content.
        
        The constructor ends with a call to self.populate, a method which should
        be overriden by subclasses.

        Args:
            parent (:obj: `Frame`): The parent frame.
            content (:obj: `object`): The content of the ScrollFrame.

        """
        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0)
        self.frame = tk.Frame(self.canvas)
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
        """Dummy populate method."""
        lbl_content = tk.Label(
            master=self.frame,
            text=str(content), 
            fg="white",
            bg="#34A2FE"
        )
        lbl_content.pack()

    def onFrameConfigure(self, event):
        """Reset the scroll region to encompass the inner frame."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


class RecipesFrame(ScrollFrame):
    """A frame containing buttons corresponding to recipes in a given Checklist.
    
    Each button toggles the corresponding recipe's "completed" state in the Checklist.

    """

    def populate(self, checklist):
        """Populates the frame with recipe buttons."""
        self.checklist = checklist
        self.buttons = dict()
        for name in checklist.recipes.keys():
            toggle_recipe = partial(self.toggle, name)
            btn_recipe = tk.Button(master=self.frame, command=toggle_recipe, text=name)
            btn_recipe.pack()
            self.buttons[name] = btn_recipe

    def toggle(self, recipe):
        """Toggles the recipe, refreshing the button and ingredients display."""
        self.checklist.toggle_recipe(recipe)
        self.refresh_button(recipe)
        self.parent.refresh_ingredients()

    def refresh_buttons(self):
        """Refreshes all buttons according to whether their recipe is complete."""
        for recipe in self.buttons:
            self.refresh_button(recipe)

    def refresh_button(self, recipe): 
        """Refreshes button display according to whether the recipe is complete."""
        button = self.buttons[recipe]
        text = ("X " + recipe) if recipe in self.checklist.completed else recipe
        button.configure(text=text)


class IngredientsFrame(ScrollFrame):
    """A frame displaying the remaining ingredients in the given Checklist."""

    def populate(self, checklist):
        """Poluplates frame with ingredient requirements."""
        self.checklist = checklist
        ingredients_string = dict_to_string(self.checklist.ingredients)
        self.lbl_ingredients = tk.Label(
            master=self.frame,
            text=ingredients_string
        )
        self.lbl_ingredients.pack()

    def refresh_ingredients(self):
        """Refreshes ingredients display."""
        ingredients_string = dict_to_string(self.checklist.ingredients)
        self.lbl_ingredients["text"] = ingredients_string
