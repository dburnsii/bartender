import json
import os
import re

root = "opendrinks/src/recipes/"

def unit_check(drink):
    ings = drink['ingredients']
    for ing in ings:
        if ing['measure']:
            if re.match(r'(fl oz|ml|tbsp|tsp|cup|cups|part)', ing['measure']):
                continue
            else:
                return False
    return True


d = os.listdir(root)
for f in d:
    if f.endswith(".json"):
        drink = json.load(open(root + f, "r"))
        if unit_check(drink):
            print(drink['name'] + " is all good.")
        else:
            print("ERROR: " + drink['name'])
