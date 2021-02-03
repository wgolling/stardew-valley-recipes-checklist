"""Main app file."""

import json
from pathlib import Path

def run():
    Checklist.cooking_checklist()
    Checklist.crafting_checklist()


class Checklist():

    def __init__(self, json_file_path):
        with open(json_file_path) as f:
            data = json.load(f)
            print(data)

    @staticmethod
    def cooking_checklist():
        path = Path(".") / "data" / "cooking_recipes.json"
        return Checklist(path)

    @staticmethod
    def crafting_checklist():
        path = Path(".") / "data" / "crafting_recipes.json"
        return Checklist(path)
