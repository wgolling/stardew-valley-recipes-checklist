import unittest

from obj.checklist import Checklist

class TestChecklist(unittest.TestCase):

    TEST_RECIPES = {
        "Foo": {"Ing1": 1, "Ing2": 2},
        "Bar": {"Ing3": 3, "Foo": 4},
        "Baz": {"Bar": 2, "Foo": 1}
    }

    def setUp(self):
        self.chkl = Checklist(TestChecklist.TEST_RECIPES)

    def test_constructor(self):
        assert(self.chkl.recipes == TestChecklist.TEST_RECIPES)
        assert(self.chkl.recipes is not TestChecklist.TEST_RECIPES)
        string_int = {
            "Buh": {"Ing": "2"}
        }
        d = Checklist(string_int)
        assert(d.recipes["Buh"]["Ing"] == 2)
        completed = {"Bar"}
        chkl = Checklist(TestChecklist.TEST_RECIPES, completed=completed)
        assert(chkl.completed == completed)

    def test_bad_constructor_input(self):
        not_a_dict = "foo"
        self.assertRaises(ValueError, Checklist, not_a_dict)

        invalid_key = {
            2: {"Ing1": 2}
        }
        self.assertRaises(ValueError, Checklist, invalid_key)

        invalid_recipe = {
            "bad_recipe": 5
        }
        self.assertRaises(ValueError, Checklist, invalid_recipe)

        invalid_ingredient = {
            "Foo": {2: 3}
        }
        self.assertRaises(ValueError, Checklist, invalid_ingredient)

        invalid_amount = {
            "Foo": {"ing": "not an int"}
        }
        self.assertRaises(ValueError, Checklist, invalid_amount)

        negative_amount = {
            "Foo": {"ing": -1}
        }
        self.assertRaises(ValueError, Checklist, negative_amount)

        not_a_set = 50
        self.assertRaises(
            TypeError, 
            Checklist,
            TestChecklist.TEST_RECIPES, 
            completed=not_a_set)

    def test_flatten_recipes_to_ingredients(self):
        expected = {
            "Ing1": 14,
            "Ing2": 28,
            "Ing3": 9
        }
        result = self.chkl.ingredients
        assert(result == expected)

    def test_toggle_recipe(self):
        self.assertRaises(ValueError, self.chkl.toggle_recipe, "Bip")
        self.chkl.toggle_recipe("Baz")
        expected = {
            "Ing1": 5,
            "Ing2": 10,
            "Ing3": 3
        }
        assert(self.chkl.ingredients == expected)
        self.chkl.toggle_recipe("Foo")
        self.chkl.toggle_recipe("Bar")
        expected = {
            "Ing1": 0,
            "Ing2": 0,
            "Ing3": 0
        }
        assert(self.chkl.ingredients == expected)
        self.chkl.toggle_recipe("Bar")
        expected = {
            "Ing1": 4,
            "Ing2": 8,
            "Ing3": 3
        }
        assert(self.chkl.ingredients == expected)
