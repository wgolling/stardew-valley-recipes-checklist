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
        # Deep copy and validate input dict at the same time.
        Checklist._validate_dict(recipes_dict)
        self.recipes = dict()
        for recipe_name, recipe in recipes_dict.items():
            recipe_name = Checklist._validate_string_key(recipe_name)
            Checklist._validate_dict(recipe)
            self.recipes[recipe_name] = dict()
            for ingredient, amount in recipe.items():
                ingredient = Checklist._validate_string_key(ingredient)
                amount = Checklist._validate_int_value(amount)
                self.recipes[recipe_name][ingredient] = amount
        Checklist._flatten_recipes_to_ingredients(self.recipes)

    @staticmethod
    def _validate_dict(input_):
        if not isinstance(input_, dict):
            raise ValueError("Expected dictionary.")

    @staticmethod
    def _validate_string_key(input_):
        if not isinstance(input_, str):
            raise ValueError("All keys must be strings.")
        return str(input_)

    @staticmethod
    def _validate_int_value(input_):
        result = None
        try:
            result = int(input_)
        except ValueError as e:
            raise ValueError("All ingredient quantities must be integers.") from e
        return result


    @staticmethod
    def _flatten_recipes_to_ingredients(data):
        pass

    def print_recipes(self):
        print(self.recipes)
