#!/usr/bin/python3

from mongoengine.queryset.visitor import Q
from flask import Flask, send_from_directory, jsonify
from flask_restful import Resource, Api, reqparse, abort
from flask_cors import CORS
from mongo import Drink, Ingredient, Valve, Config
import json

app = Flask(__name__, static_url_path='/static')
app.debug = True
app.config['SECRET_KEY'] = "testing"
app.config['MONGODB_SETTINGS'] = {'db': 'bartender'}

cors = CORS(app)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('limit', type=int, help='Max number of entries to show')
parser.add_argument('skip', type=int, help='Number of ingredients to skip')
parser.add_argument('ingredient', help='Ingredient ID')
parser.add_argument('name', help='Name to use for query')
parser.add_argument('resolve', type=int, help='Whether or not to resolve ids')
parser.add_argument('pourable', type=int, help='Whether or not to include only pourable ingredients (1=yes)')
parser.add_argument('carbonated', type=int, help='Whether or not to include carbonated ingredients (1=yes)')
parser.add_argument('key', location='headers')
parser.add_argument('value', location='headers')

@app.route('/images/<path:path>')
def send_image(path):
    return send_from_directory('/images', path)

class DrinkApi(Resource):
    def get(self, drink_id):
        drink = Drink.objects.get(id=drink_id)
        if drink:
            return json.loads(drink.to_json())
        abort(404, message="Drink {} doesn't exist".format(drink_id))

class DrinkListApi(Resource):
    def get(self):
        drinks = Drink.objects.all().only('id', 'name', 'image')
        args = parser.parse_args()
        print(args)

        if 'pourable' in args and args['pourable'] == 1:
            print("Pourable")
            list_of_drinks = []
            valves = Valve.objects(Q(ingredient__exists=True) & Q(ingredient__ne=None)).values_list('ingredient')
            print(valves)
            if not valves:
                print("Not valves")
                return []
            valve_names = list(map(lambda v: v.name, valves))
            print(valve_names)
            for drink in drinks.all_fields():
                pourable = True
                for di in drink.ingredients:
                    if not di.required:
                        continue
                    if not di.ingredient in valve_names:
                        print(di.ingredient)
                        pourable = False
                        break
                if not pourable:
                    drinks = drinks.filter(name__ne=drink.name)
                else:
                    list_of_drinks.append(drink)
            print(list_of_drinks)

        if 'skip' in args:
            drinks = drinks.skip(args['skip'])
        if 'limit' in args:
            drinks = drinks.limit(args['limit'])

        return json.loads(drinks.to_json())

class IngredientApi(Resource):
    def get(self, ingredient_id):
        ingredient = Ingredient.objects(id=ingredient_id).first()
        return json.loads(ingredient.to_json())

class IngredientListApi(Resource):
    def get(self):
        args = parser.parse_args()
        ingredients = Ingredient.objects()
        if(args['name']):
            ingredient = Ingredient.objects(name=args['name']).first()
            print(args['name'])
            return json.loads(ingredient.to_json())
        if(args['pourable']):
            ingredients = ingredients(measure="mL")
        if(args['carbonated'] == 0):
            ingredients = ingredients(carbonated=False)
        print(ingredients.all().to_json())
        return json.loads(ingredients.all().to_json())

class ValveApi(Resource):
    def get(self, valve_id):
        valves = Valve.objects(pin=valve_id)[0]
        return json.loads(valves.to_json())

    def put(self, valve_id):
        args = parser.parse_args()
        ingredient = Ingredient.objects(id=args['ingredient']).first()
        Valve.objects(pin=valve_id).update(ingredient=ingredient)
        return True

    def delete(self, valve_id):
        args = parser.parse_args()
        Valve.objects(pin=valve_id).update(ingredient=None)
        return True

class ValveListApi(Resource):
    def get(self):
        args = parser.parse_args()
        if(args['resolve']):
            valves = Valve.objects.all()
            valve_output = []
            for valve in valves:
                ing = None
                if(valve.ingredient):
                    # Convert ingredient reference to dict, and make id a string
                    ing = valve.ingredient.to_mongo().to_dict()
                    ing["id"] = str(valve.ingredient.id)
                    del ing["_id"]
                valve_output.append({"id": str(valve.id), "pin": valve.pin, "ingredient": ing})
            return valve_output
        else:
            valves = Valve.objects.all()
            return json.loads(valves.to_json()).first()

class ConfigApi(Resource):
    def get(self, key):
        if key:
            value = Config.objects(key=key)
            return  json.loads(value.to_json())[0]["value"]
        else:
            return False

    def put(self):
        args = parser.parse_args()
        if(args['key'] and args['value']):
            existing = Config.objects(key=args['key'])
            if not existing:
                Config(key=args['key'], value=args['value']).save()
                return True
            else:
                existing[0].update(value=args['value'])
                return True
        else:
            return False

    def delete(self, key):
        pass


api.add_resource(DrinkApi, '/drinks/<drink_id>')
api.add_resource(DrinkListApi, '/drinks')
api.add_resource(IngredientApi, '/ingredients/<ingredient_id>')
api.add_resource(IngredientListApi, '/ingredients')
api.add_resource(ValveApi, '/valves/<int:valve_id>')
api.add_resource(ValveListApi, '/valves')
api.add_resource(ConfigApi, '/config', '/config/<key>')

app.run(host="0.0.0.0")
