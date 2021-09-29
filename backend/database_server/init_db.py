#!/usr/bin/python3

from mongo import Ingredient, Drink, Valve, Config
import os

valveCount = 10

# TODO validate that all fields are lowercase


def validateIngredient(ing):
    if "name" not in ing:
        print("Ingredient missing name!")
        return False
    return True


Drink.objects().delete()

ing_path = os.path.join("..", "..", "opendrinks", "ingredients")
drink_path = os.path.join("..", "..", "opendrinks", "recipes")
image_path = os.path.join("..", "..", "opendrinks", "images")

ing_children = []
for ing_filename in os.listdir(ing_path):
    ing_file = open(os.path.join(ing_path, ing_filename), 'r')
    ing = Ingredient.from_json(ing_file.read())
    if(Ingredient.objects(name=ing.name)):
        # Skip, since the ingredient already exists
        # TODO: Check if any fields have been updated
        # Ingredient.objects(name=ing.name).first().modify(ing)
        continue
    ing.save()


for drink_filename in os.listdir(drink_path):
    if drink_filename == "_template.json":
        continue
    drink_file = open(os.path.join(drink_path, drink_filename))
    drink = Drink.from_json(drink_file.read())
    print(drink.name)
    drink.save()


if len(Valve.objects()) != valveCount:
    Valve.objects().delete()
    for i in range(valveCount):
        valve = Valve()
        valve.pin = i
        valve.save()


# Set up config items
# TODO: Do a real database migration
config_items = {"pin": "1234",
                "blank_time": "120",
                "screen_brightness": "100",
                "led_brightness": "100"}

for item in config_items:
    if(not Config.objects(key=item)):
        Config(key=item, value=config_items[item]).save()

print("Database all set up!")
