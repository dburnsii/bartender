#!/usr/bin/python3
"""
  Initiate or update database from opendrinks
"""

from app import (Ingredient, Drink, DrinkIngredient, DrinkAlias,
                 Valve, Config, db)
import os
import json

config_items = {"lock_pin": "",
                "blank_time": "60000",
                "screen_brightness": "100",
                "led_brightness": "100",
                "scale_calibration": "100"}


class BartenderUpdater(object):
    def __init__(self, valveCount=10):
        self.session = db.session
        self.valveCount = valveCount

        workingDir = os.path.dirname(os.path.realpath(__file__))
        self.ing_path = os.path.join(workingDir, "opendrinks", "ingredients")
        self.drink_path = os.path.join(workingDir, "opendrinks", "recipes")
        self.image_path = os.path.join(workingDir, "opendrinks", "images")

    def update_database(self):
        print("Setting up database")
        self.update_ingredients()
        self.update_drinks()
        self.update_valves()
        self.update_config()
        print("Database all set up!")

    def update_ingredients(self):
        print("Setup ingredients")
        for ing_filename in os.listdir(self.ing_path):
            ing_file = open(os.path.join(self.ing_path, ing_filename), 'r')
            ing = json.loads(ing_file.read())
            ing = Ingredient(**ing)
            if (self.session.query(Ingredient)
                    .filter(Ingredient.name == ing.name).scalar()):
                # Skip, since the ingredient already exists
                # TODO: Check if any fields have been updated
                continue
            self.session.add(ing)
        self.session.commit()

    def update_drinks(self):
        # Add drinks
        print("Setup drinks")
        for drink_filename in os.listdir(self.drink_path):
            if drink_filename == "_template.json":
                continue
            drink_file = open(os.path.join(self.drink_path, drink_filename))
            drink_dict = json.loads(drink_file.read())

            if (self.session.query(Drink)
                    .filter(Drink.name == drink_dict['name']).scalar()):
                # Skip, since the drink already exists
                # TODO: Check if any fields have been updated
                continue

            drink = Drink()
            drink.name = drink_dict['name']
            drink.image = drink_dict['image']
            drink.opendrinks = True
            for ing in drink_dict['ingredients']:
                ing_ref = self.session.query(Ingredient)\
                    .filter(Ingredient.name == ing['ingredient'])\
                    .first()
                di = DrinkIngredient(ingredient=ing_ref,
                                     quantity=ing['quantity'],
                                     required=ing['required'])
                drink.ingredients.append(di)

            for alias_str in drink_dict['alias']:
                alias = DrinkAlias(name=alias_str)
                drink.alias.append(alias)

            self.session.add(drink)
        self.session.commit()

    def update_valves(self):
        # Add valves
        print("Setup valves")
        if self.session.query(Valve).count() != self.valveCount:
            print("Clearing existing valves (if any)")
            self.session.query(Valve).delete()
            self.session.commit()
            for i in range(self.valveCount):
                valve = Valve(pin=i)
                self.session.add(valve)
        self.session.commit()

    def update_config(self):
        # Set up config items
        print("Setup config items")

        for item in config_items:
            if (not self.session.query(Config)
                    .filter(Config.key == item).scalar()):
                config = Config(key=item, value=config_items[item])
                self.session.add(config)
        self.session.commit()
