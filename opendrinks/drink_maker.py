#!/usr/bin/python3
import os
import json

ing_list = []
ing_path = "ingredients"
for ing_filename in os.listdir(ing_path):
    f = open(os.path.join(ing_path, ing_filename))
    ing = json.load(f)
    ing_list.append(ing)

print("Welcome to the Bartender drink maker!")
print("Let's start with a name for your drink")
name = input("Drink name: ").lower()

print("Alright, how about a little detail?")
description = input("Description: ").lower()

print("Great! Does this drink go by any other names? Please")
print("list them one-by-one followed by the enter key. Just")
print("press enter with the field empty when you're done.")
alias_list = []
alias = input("Alias: ").lower()
while len(alias):
    alias_list.append(alias)
    alias = input("Alias: ").lower()

print("Cool, now lets add some ingredients. Same deal here,")
print("When you get done with the igredients, just leave the ")
print("name blank and press enter.")
ingredients = []
ingredient_name = input("Ingredient name: ").lower()
while len(ingredient_name):
    ingredient_object = \
        next((ing for ing in ing_list if ing["name"] == ingredient_name), None)
    if not ingredient_object:
        ingredient_object = {}
        print("Uh oh! We don't know about {} just yet!".
              format(ingredient_name))
        print("We can add it now. First, we'll need to know how you'd measure "
              "this. \nWith things like lemon wedges and ice\n"
              "cubes, we normally use \"count\". For things like liqour and "
              "soda, we'll use \"mL\". For things we only need a dash of like "
              "bitters, we'll use \"dash\".\n Select one of the following:\n"
              "[1] mL\n[2] dash\n[3] count")
        measure = input("measure: ")
        carbonated_boolean = False
        if measure == "1":
            measure_type = "mL"
            carbonated = input("Is this ingredient carbonated? Even a little "
                               "bit? (yes/no): ")
            if carbonated.lower() == "y" or carbonated.lower() == "yes":
                carbonated_boolean = True
            elif carbonated.lower() == "n" or carbonated.lower() == "no":
                carbonated_boolean = False
            else:
                print("Invalid input ({}). Try again.".format(carbonated))
                continue
        elif measure == "2":
            measure_type = "dash"
        elif measure == "3":
            measure_type = "count"
        else:
            print("Invalid response ({})".format(measure))
            continue
        ingredient_object['name'] = ingredient_name
        ingredient_object['measure'] = measure_type
        if measure_type == "mL":
            ingredient_object["carbonated"] = carbonated_boolean
        print(json.dumps(ingredient_object))

        # TODO: further validate ingredient name for filename
        ing_file = open(os.path.join(ing_path,
                                     ingredient_name.replace(" ", "_") +
                                     ".json"),
                        "w")
        json.dump(ingredient_object, ing_file)
        ing_file.close()
        print("All done adding {}!".format(ingredient_name))
    else:
        print(ingredient_object)
    drink_ingredient = {}
    drink_ingredient["ingredient"] = ingredient_object["name"]
    drink_ingredient["quantity"] = \
        float(input("Cool, how much should we add? ({}): ".
                    format(ingredient_object["measure"])))
    required = \
        input("Is this ingredient required to make this drink? (yes/no): ")
    while 'required' not in drink_ingredient:
        if required.lower() == "y" or required.lower() == "yes":
            drink_ingredient['required'] = True
        elif required.lower() == "n" or required.lower() == "no":
            drink_ingredient['required'] = False
        else:
            print("Invalid input ({}). Try again.".format(required))
    ingredients.append(drink_ingredient)
    print("Ingredient added!")
    print("When you get done with the igredients, just leave the ")
    print("name blank and press enter.")
    ingredient_name = input("Ingredient name: ").lower()

drink = {}
drink['name'] = name
drink['ingredients'] = ingredients
drink['alias'] = alias_list
drink_name_clean = name.replace(' ', '_')
drink['image'] = drink_name_clean + ".jpg"

print(json.dumps(drink))
drink_file = open(os.path.join('recipes', drink_name_clean + '.json'), 'w')
json.dump(drink, drink_file)
drink_file.close()
