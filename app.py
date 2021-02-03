"""Main app file."""

import json
from pathlib import Path

def run():
    data_path = Path(".") / "data"
    cook = Checklist(load_json(data_path / "cooking_recipes.json"))
    cook.print_recipes()
    crft = Checklist(load_json(data_path / "crafting_recipes.json"))
    crft.print_recipes()

def load_json(file_path):
    data = None
    with open(file_path) as f:
        data = json.load(f)
    return data

def add_key_value_to_dict(k, v, d):
    if k not in d:
        d[k] = 0
    d[k] += v

def add_dicts(d1, d2, multiplier=1):
    for k, v in d2.items():
        add_key_value_to_dict(k, multiplier * v, d1)


class Checklist():

    def __init__(self, recipes_dict):
        self.recipes = dict(recipes_dict)
        Checklist._flatten_recipes_to_ingredients(self.recipes)

    @staticmethod
    def _flatten_recipes_to_ingredients(data):
        pass

    def print_recipes(self):
        print(self.recipes)
