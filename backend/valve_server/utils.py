import requests

pourable_ingredients = []


def grab_valves():
    req = requests.get("http://localhost:5000/valves?resolve=1")
    req_json = req.json()
    for i in range(len(req_json)-1, -1, -1):
        if("ingredient" not in req_json[i] or
           req_json[i]["ingredient"] is None):
            del req_json[i]
    return req_json


def variance(value):
    return max(value) - min(value)


def grab_drink(id):
    req = requests.get("http://localhost:5000/drinks/{}".format(id))
    req_json = req.json()
    return req_json


def grab_pourable_ingredients():
    global pourable_ingredients
    if len(pourable_ingredients) == 0:
        req = requests.get("http://localhost:5000/ingredients?pourable=1")
        req_json = req.json()
        pourable_ingredients = req_json
        return req_json
    else:
        return pourable_ingredients


def ing_available(ingredient, valves):
    return any(map((lambda x:
                    ingredient["ingredient"] == x['ingredient']['name']),
               valves))


def ing_pourable(ingredient):
    pourable = grab_pourable_ingredients()
    for ing in pourable:
        if ing["name"] == ingredient["ingredient"]:
            return ing["measure"] == "mL"
    return False


def remaining_in_queue(queue):
    return sum(map(lambda x: x['quantity'], queue))


def create_drink_queue(ingredients, valves):
    print(ingredients)
    output = []
    total = 0
    for ingredient in ingredients:
        valve = None
        try:
            valve = next(
                valve for valve in valves if
                valve['ingredient']['id'] == ingredient['ingredient_id'])
        except Exception as e:
            print(e)
            if ingredient['ingredient']['carbonated'] is True:
                print("Skipping carbonated")
                valve = {}
                valve['pin'] = None
            elif ingredient['required'] is False:
                print("Skipping non-required ingredient")
                continue
            elif ingredient['ingredient']['measure'] != "mL":
                print("Skipping non-liquid ingredient")
                continue
            else:
                return None
            pass
        output.append(
            {'pin': valve['pin'], 'quantity': ingredient['quantity'], 'name': ingredient['ingredient']['name']})
        total += ingredient['quantity']
    return (output, total)
