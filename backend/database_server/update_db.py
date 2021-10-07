#!/usr/bin/python3
"""
  Initiate or update database from opendrinks
"""

from app import (Ingredient, Drink, DrinkIngredient, DrinkAlias,
                 Valve, Config, db)
import os
import json

s = db.session
valveCount = 10

ing_path = os.path.join("..", "..", "opendrinks", "ingredients")
drink_path = os.path.join("..", "..", "opendrinks", "recipes")
image_path = os.path.join("..", "..", "opendrinks", "images")


print("Setting up database")

# Add ingredients
print("Setup ingredients")
for ing_filename in os.listdir(ing_path):
    ing_file = open(os.path.join(ing_path, ing_filename), 'r')
    ing = json.loads(ing_file.read())
    ing = Ingredient(**ing)
    if(s.query(Ingredient).filter(Ingredient.name == ing.name).scalar()):
        # Skip, since the ingredient already exists
        # TODO: Check if any fields have been updated
        continue
    s.add(ing)
s.commit()


# Add drinks
print("Setup drinks")
for drink_filename in os.listdir(drink_path):
    if drink_filename == "_template.json":
        continue
    drink_file = open(os.path.join(drink_path, drink_filename))
    drink_dict = json.loads(drink_file.read())

    if(s.query(Drink).filter(Drink.name == drink_dict['name']).scalar()):
        # Skip, since the drink already exists
        # TODO: Check if any fields have been updated
        continue

    drink = Drink()
    drink.name = drink_dict['name']
    drink.image = drink_dict['image']
    for ing in drink_dict['ingredients']:
        ing_ref = s.query(Ingredient)\
                   .filter(Ingredient.name == ing['ingredient'])\
                   .first()
        di = DrinkIngredient(ingredient=ing_ref,
                             quantity=ing['quantity'],
                             required=ing['required'])
        drink.ingredients.append(di)

    for alias_str in drink_dict['alias']:
        alias = DrinkAlias(name=alias_str)
        drink.alias.append(alias)

    s.add(drink)
s.commit()

# Add valves
print("Setup valves")
if s.query(Valve).count() != valveCount:
    print("Clearing existing valves (if any)")
    s.query(Valve).delete()
    s.commit()
    for i in range(valveCount):
        valve = Valve(pin=i)
        s.add(valve)
s.commit()


# Set up config items
print("Setup config items")
config_items = {"pin": "1234",
                "blank_time": "120",
                "screen_brightness": "100",
                "led_brightness": "100"}

for item in config_items:
    if(not s.query(Config).filter(Config.key == item).scalar()):
        config = Config(key=item, value=config_items[item])
        s.add(config)
s.commit()


print("Database all set up!")
