"""Recipes and ingredients checklist.

This module provides a Checklist object for determing the raw ingredients
required to complete multiple recipes.

"""

from lib.util import add_key_value_to_dict, add_dicts


class Checklist():
    """Manages a dictionary of recipes and a checklist of ingredients.
    
    Attributes:
        recipes (dict): A dictionary representing a collection of recipes.
        completed (set): A set containing the recipes that have been compelted.
        ingredients (dict): A dictionary of raw ingredients and the quantities
            needed to complete all of the recipes.
    
    """

    def __init__(self, recipes_dict, completed=None):
        """Constructs a Checklist object given a dictionary of recipes.
        
        Args:
            recipes_dict (dict): A dictionary representing a collection of
                recipes. The keys are recipe names as strings, and each value
                is itself a dictionary, whose keys are ingredient name strings
                and whose values are non-negative integers.
            completed (:obj:`set`, optional): A set of recipes that are already completed.

        Raises:
            ValueError: If `recipes_dict` is not a dictionary.
            ValueError: If the keys of `recipes_dict` are not strings.
            ValueError: If the values of `recipes_dict` are not dictionaries.
            ValueError: If `recipes_dict`'s values keys are not strings.
            ValueError: If `recipes_dict`'s values' values are not ints.
            TypeError: If `completed` is not iterable.
     
        """
        self.recipes = Checklist._validate_input(recipes_dict)
        self.completed = set()
        if completed != None:
            for recipe in completed:
                if recipe in self.recipes:
                    self.completed.add(recipe)
        self.ingredients = Checklist._flatten_recipes_to_ingredients(self.recipes)

    @staticmethod
    def _validate_input(recipes_dict):
        """Deep copy and validate input dictionary at the same time."""
        Checklist._validate_dict(recipes_dict)
        result = dict()
        for recipe_name, recipe in recipes_dict.items():
            recipe_name = Checklist._validate_string_key(recipe_name)
            result[recipe_name] = Checklist._validate_recipe(recipe)
        return result

    @staticmethod
    def _validate_recipe(recipe):
        """Checks that the keys are strings and the values are intable."""
        Checklist._validate_dict(recipe)
        result = dict()
        for ingredient, amount in recipe.items():
            ingredient  = Checklist._validate_string_key(ingredient)
            amount      = Checklist._validate_int_value(amount)
            result[ingredient] = amount
        return result

    @staticmethod
    def _validate_dict(input_):
        """Raises ValueError if input is not a dictionary."""
        if not isinstance(input_, dict):
            raise ValueError("Expected dictionary.")

    @staticmethod
    def _validate_string_key(key):
        """Raises ValueError if the given key is not a string, otherwise returns a copy."""
        if not isinstance(key, str):
            raise ValueError("All keys must be strings.")
        return str(key)

    @staticmethod
    def _validate_int_value(value):
        """Raises ValueError if the given value is not convertible to int, otherwise returns an in copy."""
        result = None
        try:
            result = int(value)
        except ValueError as e:
            raise ValueError("All ingredient quantities must be integers.") from e
        if result < 0:
            raise ValueError("All ingredient quantities must be non-negative.")
        return result

    @staticmethod
    def _flatten_recipes_to_ingredients(recipes_table):
        """Given a recipes table, returns the table of raw ingredient requirements."""
        result = dict()
        for recipe in recipes_table.values():
            ingredients = Checklist._get_raw_ingredients(recipe, recipes_table)
            add_dicts(result, ingredients)
        return result

    @staticmethod
    def _get_raw_ingredients(recipe, recipes_table):
        """Recursively flattens recipe dictionaries."""
        result = dict()
        for ing, amt in recipe.items():
            # Check if the ingredient is itself a recipe.
            if ing in recipes_table:
                d = Checklist._get_raw_ingredients(
                        recipes_table[ing], 
                        recipes_table
                    )
                add_dicts(result, d, multiplier=amt)
            else:
                add_key_value_to_dict(ing, amt, result)
        return result

    def toggle_recipe(self, recipe_string):
        """Marks/unmarks the given recipe as complete and updates the ingredients table.
        
        Args:
            recipe_string (str): The name of the recipe.

        Raises:
            ValueError: If `recipe_string` is not in the recipes table.

        """
        if recipe_string not in self.recipes:
            raise ValueError("Recipe not recognized.")
        if recipe_string in self.completed:
            self.completed.remove(recipe_string)
            sign = 1
        else:
            self.completed.add(recipe_string)
            sign = -1
        recipe = self.recipes[recipe_string]
        raw_ingredients = self._get_raw_ingredients(recipe, self.recipes)
        add_dicts(self.ingredients, raw_ingredients, multiplier=sign)
