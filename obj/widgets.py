"""Custom widgets for the user interface."""

import tkinter as tk

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
