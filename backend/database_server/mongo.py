
import mongoengine as me

me.connect('bartender')


class Ingredient(me.Document):
    name = me.StringField(required=True)
    measure = me.StringField(required=True)
    carbonated = me.BooleanField()
    parent = me.ReferenceField("self")


class DrinkIngredient(me.EmbeddedDocument):
    ingredient = me.StringField(required=True)
    quantity = me.FloatField(required=True)
    required = me.BooleanField(required=False, default=True)


class Drink(me.Document):
    name = me.StringField(required=True)
    image = me.StringField(required=True)
    alias = me.ListField()
    ingredients = me.ListField(me.EmbeddedDocumentField(DrinkIngredient))
    opendrinks = me.BooleanField(required=True, default=True)


class Valve(me.Document):
    pin = me.IntField()
    ingredient = me.ReferenceField(Ingredient)


class Config(me.Document):
    key = me.StringField(required=True)
    value = me.StringField(required=True)
