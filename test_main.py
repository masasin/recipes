import unittest
from unittest.mock import MagicMock
import main


class FoodTest(unittest.TestCase):
    def setUp(self):
        self.food = main.FoodCategory("Food")

    def test_init(self):
        self.assertEqual(self.food.name, "Food")
        self.assertEqual(self.food.density, 1000)
        self.assertEqual(self.food.usability, 1)
        self.assertEqual(self.food.nutrition, {})


class VendorTest(unittest.TestCase):
    item1 = MagicMock(spec=main.Ingredient)
    item2 = MagicMock(spec=main.Ingredient)

    def setUp(self):
        self.vendor = main.Vendor("Gyomu", "9", "226", "gyomu@gmail.com")

    def test_init(self):
        self.assertEqual(self.vendor.name, "Gyomu")
        self.assertEqual(self.vendor.address, "9")
        self.assertEqual(self.vendor.phone, "226")
        self.assertEqual(self.vendor.email, "gyomu@gmail.com")
        self.assertEqual(self.vendor.inventory, {})

    def test_add_add_item(self):
        self.vendor.add_item(self.item1, 12, date="2014")
        self.assertEqual(self.vendor.inventory, {self.item1: [[12, "2014"]]})

    def test_add_two_items(self):
        self.vendor.add_item(self.item1, 12, date="2014")
        self.vendor.add_item(self.item2, 15, date="2014")
        self.assertEqual(self.vendor.inventory, {self.item1: [[12, "2014"]],
                                                 self.item2: [[15, "2014"]]})

    def test_update_item_price(self):
        self.vendor.add_item(self.item1, 12, date="2014")
        self.vendor.add_item(self.item1, 15, date="2015")
        self.assertEqual(self.vendor.inventory, {self.item1: [[12, "2014"],
                                                              [15, "2015"]]})


class IngredientTest(unittest.TestCase):
    vendor1 = MagicMock(spec=main.Vendor)
    vendor2 = MagicMock(spec=main.Vendor)
    milk = MagicMock(spec=main.FoodCategory, nutrition={})

    def setUp(self):
        self.morinaga_milk = main.Ingredient("Morinaga Milk", self.milk, 1000)

    def test_init(self):
        self.assertEqual(self.morinaga_milk.name, "Morinaga Milk")
        self.assertEqual(self.morinaga_milk.food, self.milk)
        self.assertEqual(self.morinaga_milk.mass, 1000)
        self.assertEqual(self.morinaga_milk.nutrition, {})
        self.assertEqual(self.morinaga_milk.vendors, {})
        self.assertEqual(self.morinaga_milk.price, 0)
        self.assertEqual(self.morinaga_milk.vendor, None)
        self.assertEqual(self.morinaga_milk.price_updated, None)
        self.assertEqual(self.morinaga_milk.unit_price, 0)

    def test_add_item(self):
        self.morinaga_milk.update_price(self.vendor1, 12, "2014")
        self.vendor1.add_item.assert_called_once_with(self.morinaga_milk, 12, "2014")
        self.assertEqual(self.morinaga_milk.vendors, {self.vendor1: [[12, "2014"]]})

    def test_add_two_vendors(self):
        self.morinaga_milk.update_price(self.vendor1, 12, "2014")
        self.vendor1.add_item.assert_called_with(self.morinaga_milk, 12, "2014")
        self.morinaga_milk.update_price(self.vendor2, 13, "2014")
        self.vendor2.add_item.assert_called_with(self.morinaga_milk, 13, "2014")
        self.assertEqual(self.morinaga_milk.vendors, {self.vendor1: [[12, "2014"]],
                                                      self.vendor2: [[13, "2014"]]})

    def test_update_vendor_price(self):
        self.morinaga_milk.update_price(self.vendor1, 12, "2014")
        self.vendor1.add_item.assert_called_with(self.morinaga_milk, 12, "2014")
        self.morinaga_milk.update_price(self.vendor1, 13, "2015")
        self.assertEqual(self.morinaga_milk.vendors, {self.vendor1: [[12, "2014"],
                                                                     [13, "2015"]]})
        self.vendor1.add_item.assert_called_with(self.morinaga_milk, 13, "2015")

    def test_set_current_price_init(self):
        self.morinaga_milk.update_price(self.vendor1, 12, "2014")
        self.assertEqual(self.morinaga_milk.price, 12)
        self.assertEqual(self.morinaga_milk.vendor, self.vendor1)
        self.assertEqual(self.morinaga_milk.price_updated, "2014")
        self.assertEqual(self.morinaga_milk.unit_price, 0.012)

    def test_set_current_price_no_change(self):
        self.morinaga_milk.update_price(self.vendor1, 12, "2014")
        self.morinaga_milk.update_price(self.vendor2, 14, "2014")
        self.assertEqual(self.morinaga_milk.price, 12)
        self.assertEqual(self.morinaga_milk.vendor, self.vendor1)
        self.assertEqual(self.morinaga_milk.price_updated, "2014")
        self.assertEqual(self.morinaga_milk.unit_price, 0.012)

    def test_set_current_price_default(self):
        self.morinaga_milk.update_price(self.vendor1, 12, "2014")
        self.morinaga_milk.update_price(self.vendor2, 14, "2015", default=True)
        self.assertEqual(self.morinaga_milk.price, 14)
        self.assertEqual(self.morinaga_milk.vendor, self.vendor2)
        self.assertEqual(self.morinaga_milk.price_updated, "2015")
        self.assertEqual(self.morinaga_milk.unit_price, 0.014)

    def test_price_list(self):
        self.morinaga_milk.update_price(self.vendor1, 12, "2014")
        self.morinaga_milk.update_price(self.vendor1, 15, "2015")
        self.morinaga_milk.update_price(self.vendor2, 13, "2014")
        price_list = self.morinaga_milk.get_price_list()
        self.assertEqual(price_list, {self.vendor1: [15, "2015"],
                                      self.vendor2: [13, "2014"]})

    def test_price_list_no_vendors_yet(self):
        price_list = self.morinaga_milk.get_price_list()
        self.assertEqual(price_list, {})


class RecipeTest(unittest.TestCase):
    item1 = MagicMock(spec=main.Ingredient, mass=500, unit_price=0.02)
    item2 = MagicMock(spec=main.Ingredient, mass=1000, unit_price=0.015)

    def setUp(self):
        self.recipe = main.Recipe("Recipe", 10, 15)

    def test_init(self):
        self.assertEqual(self.recipe.name, "Recipe")
        self.assertEqual(self.recipe.prep_time, 10)
        self.assertEqual(self.recipe.cooking_time, 15)
        self.assertEqual(self.recipe.ingredients, {})

    def test_add_ingredient(self):
        self.recipe.add_ingredient(self.item1, 300)
        self.assertEqual(self.recipe.ingredients, {self.item1: 300})

    def test_add_two_ingredients(self):
        self.recipe.add_ingredient(self.item1, 300)
        self.recipe.add_ingredient(self.item2, 500)
        self.assertEqual(self.recipe.ingredients, {self.item1: 300,                                                   self.item2: 500})

    def test_add_more_of_same_ingredient(self):
        self.recipe.add_ingredient(self.item1, 300)
        self.recipe.add_ingredient(self.item1, 500)
        self.assertEqual(self.recipe.ingredients, {self.item1: 800})

    def test_get_price(self):
        self.recipe.add_ingredient(self.item1, 300)
        self.recipe.add_ingredient(self.item2, 500)
        price = self.recipe.get_price()
        self.assertEqual(price, 13.5)

    def test_get_mass(self):
        self.recipe.add_ingredient(self.item1, 300)
        self.recipe.add_ingredient(self.item2, 500)
        mass = self.recipe.get_mass()
        self.assertEqual(mass, 800)

    def test_get_vals_empty(self):
        self.assertEqual(self.recipe.get_price(), 0)
        self.assertEqual(self.recipe.get_mass(), 0)


if __name__ == "__main__":
    unittest.main()
