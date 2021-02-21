import json

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

def dict_to_string(d):
    """Returns a readable string representing a dictionary."""
    result = ""
    for k, v in d.items():
        if v == 0:
            continue
        result += str(k) + ": " + str(v) + "\n"
    return result

def load_json(file_path):
    """Tries to load the json in the given file path."""
    data = None
    with open(file_path) as f:
        data = json.load(f)
    return data
