"""Main app file."""

import json
from pathlib import Path

from obj.checklist import Checklist

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
