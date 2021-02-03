import unittest

from app import Checklist

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
