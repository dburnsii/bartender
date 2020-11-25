#!/usr/bin/python3

from mongo import *
import os
import json

valveCount = 10

# TODO validate that all fields are lowercase
def validateIngredient(ing):
    if not "name" in ing:
        print("Ingredient missing name!")
        return False
    return True

Ingredient.objects().delete()
Drink.objects().delete()

# TODO: Handle these two more gracefully to preserve user set fields
Valve.objects().delete()
Config.objects().delete()

ing_path = os.path.join("..", "..", "opendrinks", "ingredients")
drink_path = os.path.join("..", "..", "opendrinks", "recipes")
image_path = os.path.join("..", "..", "opendrinks", "images")

ing_children = []
for ing_filename in os.listdir(ing_path):
    ing_file = open(os.path.join(ing_path, ing_filename), 'r')
    ing = Ingredient.from_json(ing_file.read())
    ing.save()


for drink_filename in os.listdir(drink_path):
    if drink_filename == "_template.json":
        continue
    print("Processing {}".format(drink_filename))
    drink_file = open(os.path.join(drink_path, drink_filename))
    drink = Drink.from_json(drink_file.read())
        #ing_name = ing['ingredient']
        #ing_reference = Ingredient.objects(name=ing_name).first()
        #print(ing_reference)
        #ing.ingredient = ing_reference
    drink.save()
    for ing in drink.ingredients:
        print(ing)
    print(drink.to_json())

for i in range(valveCount):
    valve = Valve()
    valve.pin = i
    valve.save()

Config(key="pin", value="1234").save()
Config(key="blank_time", value="120").save()

print("Database all set up!")
