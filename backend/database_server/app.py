from flask import Flask, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade, current
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
from dataclasses import dataclass
from sqlalchemy import or_, null, create_engine
import update

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///.bartender.db"

db = SQLAlchemy(app, engine_options="")
migrate = Migrate(app, db)
cors = CORS(app)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('limit', type=int, help='Max number of entries to show')
parser.add_argument('skip', type=int, help='Number of ingredients to skip')
parser.add_argument('ingredient', help='Ingredient ID')
parser.add_argument('name', help='Name to use for query')
parser.add_argument('resolve', type=int, help='Whether or not to resolve ids')
parser.add_argument('pourable', type=int,
                    help='Whether or not to include only pourable '
                         'ingredients (1=yes)')
parser.add_argument('carbonated', type=int,
                    help='Whether or not to include carbonated '
                         'ingredients (1=yes)')
parser.add_argument('key', location='headers')
parser.add_argument('value', location='headers')


# Models
@dataclass
class Ingredient(db.Model):
    # Mapping for JSON
    id: int
    name: str
    measure: str
    carbonated: bool

    # Mapping for sqlite
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    measure = db.Column(db.String(32), nullable=False)
    carbonated = db.Column(db.Boolean, nullable=False, default=False)


@dataclass
class DrinkIngredient(db.Model):
    id: int
    ingredient: dict
    ingredient_id: int
    drink_id: int
    quantity: float
    required: bool

    id = db.Column(db.Integer, primary_key=True)
    ingredient = db.relationship('Ingredient')
    ingredient_id = db.Column(db.Integer,
                              db.ForeignKey('ingredient.id'),
                              nullable=False)
    drink_id = db.Column(db.Integer, db.ForeignKey('drink.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    required = db.Column(db.Boolean, nullable=False)


@dataclass
class DrinkAlias(db.Model):
    id: int
    drink_id: int
    name: str

    id = db.Column(db.Integer, primary_key=True)
    drink_id = db.Column(db.Integer, db.ForeignKey('drink.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)


@dataclass
class Drink(db.Model):
    id: int
    name: str
    image: str
    alias: list
    ingredients: list
    opendrinks: bool

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(1024))
    alias = db.relationship('DrinkAlias')
    ingredients = db.relationship('DrinkIngredient')
    opendrinks = db.Column(db.Boolean, default=True)


@dataclass
class Valve(db.Model):
    id: int
    pin: int
    ingredient: dict
    ingredient_id: int

    id = db.Column(db.Integer, primary_key=True)
    pin = db.Column(db.Integer)
    ingredient = db.relationship('Ingredient')
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'))


@dataclass
class Config(db.Model):
    id: int
    key: str
    value: str

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(255), nullable=False)
    value = db.Column(db.String(255), nullable=False)


# Image resources
@app.route('/images/<path:path>')
def send_image(path):
    return send_from_directory('/images', path)


class DrinkApi(Resource):
    def get(self, drink_id):
        return jsonify(Drink.query.filter(Drink.id == drink_id).first_or_404())


class DrinkListApi(Resource):
    def get(self):
        drink_q = Drink.query
        args = parser.parse_args()
        print(args)

        carbonated = True

        if 'pourable' in args and args['pourable'] == 1:
            print("Pourable")
            # Grab all the ingredient id's that are loaded to a valve
            available_ingredient_q = \
                Ingredient.query.join(Valve).with_entities(Ingredient.id)

            carbonated_ingredient_q = \
                Ingredient.query.filter(
                    Ingredient.carbonated is True).with_entities(Ingredient.id)
            # Find all the drink_ingredients that are missing
            drink_ingredient_q = \
                DrinkIngredient.query.\
                filter(DrinkIngredient.required is True).\
                filter(DrinkIngredient.ingredient_id.
                       not_in(available_ingredient_q)).\
                filter(DrinkIngredient.ingredient_id.
                       not_in(carbonated_ingredient_q)).\
                join(Drink).with_entities(Drink.id)
            # Filter drinks by those that aren't missing required ingredients
            drink_q = drink_q.filter(Drink.id.not_in(drink_ingredient_q))

        if 'skip' in args:
            drink_q = drink_q.offset(args['skip'])
        if 'limit' in args:
            drink_q = drink_q.limit(args['limit'])

        return jsonify(drink_q.all())


class IngredientApi(Resource):
    def get(self, ingredient_id):
        return jsonify(db.session.query(Ingredient).all())


class IngredientListApi(Resource):
    def get(self):
        args = parser.parse_args()
        ingredients_q = Ingredient.query
        if (args['name']):
            ingredient = Ingredient.query(Ingredient.name == args['name'])\
                                   .first_or_404()
            return jsonify(ingredient)
        if (args['pourable']):
            ingredients_q = ingredients_q.filter(Ingredient.measure == "mL")
        if (args['carbonated'] == 0):
            ingredients_q = ingredients_q.filter(
                Ingredient.carbonated is False)
        return jsonify(ingredients_q.all())


class ValveApi(Resource):
    def get(self, valve_id):
        return (jsonify(Valve.query.filter(Valve.pin == valve_id)
                .first_or_404()))

    def put(self, valve_id):
        args = parser.parse_args()
        i = Ingredient.query.filter(
            Ingredient.id == args['ingredient']).first()
        Valve.query.filter(
            Valve.pin == valve_id).update({Valve.ingredient_id: i.id})
        db.session.commit()
        return True

    def delete(self, valve_id):
        Valve.query.filter(
            Valve.pin == valve_id).update({Valve.ingredient_id: null()})
        db.session.commit()
        return True


class ValveListApi(Resource):
    def get(self):
        args = parser.parse_args()
        if (args['resolve']):
            pass
        return jsonify(Valve.query.all())


class ConfigApi(Resource):
    def get(self, key):
        if key:
            config = Config.query.filter(Config.key == key).first_or_404()
            return config.value
        else:
            return None

    def put(self):
        args = parser.parse_args()
        if (args['key'] and args['value']):
            existing = Config.query.filter(Config.key == args['key'])
            if not existing.scalar():
                db.session.add(Config(key=args['key'], value=args['value']))
                db.session.commit()
                return True
            else:
                existing.update({Config.value: args['value']})
                db.session.commit()
                return True
        else:
            return False

    def delete(self, key):
        if (key):
            existing = Config.query.filter(Config.key == key).first()
            if existing:
                db.session.delete(existing)
                db.session.commit()
                return True
            else:
                return False
        else:
            return False


api.add_resource(DrinkApi, '/drinks/<int:drink_id>')
api.add_resource(DrinkListApi, '/drinks')
api.add_resource(IngredientApi, '/ingredients/<int:ingredient_id>')
api.add_resource(IngredientListApi, '/ingredients')
api.add_resource(ValveApi, '/valves/<int:valve_id>')
api.add_resource(ValveListApi, '/valves')
api.add_resource(ConfigApi, '/config', '/config/<string:key>')

if __name__ == '__main__':
    create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    with app.app_context():
        upgrade()
    updater = update.BartenderUpdater()
    updater.update_database()
    app.run(host="0.0.0.0", debug=True)
