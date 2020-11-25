import urllib.request
import json
import os
import multiprocessing as mp
import time

def get_drink_full(drink_id):
    url ="https://www.thecocktaildb.com/api/json/v2/{}/lookup.php?i={}".format(drink_id[1], drink_id[0])
    drink_json = urllib.request.urlopen(url).read()
    drink_full = json.loads(drink_json)['drinks'][0]
    if 'strDrinkThumb' in drink_full and drink_full['strDrinkThumb']:
        image = urllib.request.urlopen(drink_full['strDrinkThumb']+ "/preview").read()
        with open("images/drink_{}.jpg".format(drink_id[0]), "wb") as f:
            f.write(image)
            f.close()
    return drink_full

def get_ingredient_full(drink_id):
    url = "https://www.thecocktaildb.com/api/json/v2/{}/search.php?{}".format(drink_id[1], urllib.parse.urlencode({'i': drink_id[0]}))
    drink_json = urllib.request.urlopen(url).read()
    if drink_json:
        drink_full = json.loads(drink_json)['ingredients'][0]
        return drink_full
    else:
        return {}


if __name__ == '__main__':
    api_key = ""
    if not os.getenv('COCKTAIL_API_KEY'):
        print("Please set 'COCKTAIL_API_KEY' to pull drinks")
        exit(1)
    else:
        api_key = os.getenv('COCKTAIL_API_KEY')

    full_drinks = []

    drinks_json = urllib.request.urlopen("https://www.thecocktaildb.com/api/json/v2/{}/filter.php?a=Alcoholic".format(api_key)).read()
    drinks = json.loads(drinks_json)['drinks']
    
    print("Grabbing full details for {} drinks.".format(len(drinks)))
    drink_ids = map(lambda d: (d['idDrink'], api_key), drinks)
    with mp.Pool(processes=8) as pool:
        full_drinks = pool.map(get_drink_full, drink_ids) 

    drinks_file = open("drinks.json", "w")
    drinks_file.write(json.dumps(full_drinks))
    drinks_file.close()

    full_ing = []

    ings_json = urllib.request.urlopen("https://www.thecocktaildb.com/api/json/v2/{}/list.php?i=list".format(api_key)).read()
    ings = json.loads(ings_json)['drinks']

    print("Grabbing full details for {} ingredients.".format(len(ings)))
    ing_ids = map(lambda d: (d['strIngredient1'], api_key), ings)
    with mp.Pool(processes=8) as pool:
        full_ing = pool.map(get_ingredient_full, ing_ids)

    ing_file = open("ingredients.json", "w")
    ing_file.write(json.dumps(full_ing))
    ing_file.close()
