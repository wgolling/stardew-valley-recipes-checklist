"""Recipes and ingredients checklist.

This module provides a Checklist object for determing the raw ingredients
required to complete multiple recipes.

"""

def add_key_value_to_dict(k, v, d):
    """Adds a key value pair to a dictionary with integer values.

    The function alters the given dictionary.
    
    Args:
        k: An arbitrary key
        v (int): An integer value
        d (dict): A dictionary with integer values.
    
    """
    if k not in d:
        d[k] = 0
    d[k] += v

def add_dicts(d1, d2, multiplier=1):
    """Adds two dictionaries key-wise.

    For each key value pair in the second dictionary, the value is added to the
    value for that key in the first dictionary (with a default value of 0).
    There is an optional multiplier argument which multiplies the values in
    the secdon dictionary.
    
    Args:
        d1 (dict): A dictionary with integer values.
        d2 (dict): A dictionary with integer values.
        multiplier (:obj:`int`, optional): Multiplies the values of d2.
    
    """
    for k, v in d2.items():
        add_key_value_to_dict(k, multiplier * v, d1)


class Checklist():
    """Manages a dictionary of recipes and a checklist of ingredients.
    
    Attributes:
        recipes (dict): A dictionary representing a collection of recipes.
        ingredients (dict): A dictionary of raw ingredients and the quantities
            needed to complete all of the recipes.
    
    """

    def __init__(self, recipes_dict):
        """Construsts a Checklist object given a dictionary of recipes.
        
        Args:
            recipes_dict (dict): A dictionary representing a collection of recipes.
                The keys are recipes names as strings, and each value is itself a
                dictionary, whose keys are ingredient name strings and whose values
                are non-negative integers.
        
        """
        self.recipes = Checklist._validate_input(recipes_dict)
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

    def print_recipes(self):
        print(self.recipes)
