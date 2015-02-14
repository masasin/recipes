from datetime import date


class Vendor:
    def __init__(self, name, address, phone, email):
        self.name = name
        self.address = address
        self.phone = phone
        self.email = email
        self.inventory = {}

    def add_item(self, item, price, date=date.today()):
        self.inventory.setdefault(item, []).append([price, date])


class FoodCategory:
    def __init__(self, name, density=1000, usability=1, nutrition={}):
        self.name = name
        self.density = density
        self.usability = usability
        self.nutrition = nutrition


class Ingredient:
    def __init__(self, name, food, mass, nutrition=None, upc=None):
        self.name = name
        self.food = food
        self.mass = mass
        self.vendors = {}
        if nutrition is None:
            self.nutrition = food.nutrition
        else:
            self.nutrition = nutrition
        self.price = 0
        self.vendor = None
        self.price_updated = None
        self.unit_price = 0

    def update_price(self, vendor, price, date=date.today(), default=False):
        self.vendors.setdefault(vendor, []).append([price, date])
        vendor.add_item(self, price, date)
        if default or not self.price or not self.vendor or not self.price_updated:
            self.price = price
            self.vendor = vendor
            self.price_updated = date
            self.unit_price = price / self.mass

    def get_price_list(self):
        price_list = {}
        for vendor, data in self.vendors.items():
            price_list[vendor] = data[-1]
        return price_list


class Recipe:
    def __init__(self, name, prep_time=0, cooking_time=0):
        self.name = name
        self.prep_time = prep_time
        self.cooking_time = cooking_time
        self.ingredients = {}

    def add_ingredient(self, ingredient, amount):
        self.ingredients[ingredient] = self.ingredients.setdefault(
            ingredient, 0) + amount

    def get_price(self):
        return sum(ingredient.unit_price * amount for ingredient, amount in self.ingredients.items())

    def get_mass(self):
        return sum(self.ingredients.values())
