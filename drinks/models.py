from django.db import models
import json


class IngredientsField(models.Field):
    description = "A list of ingredients and quantities"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        return name, path, args, kwargs

    def db_type(self, connection):
        return 'varchar'

    def rel_db_type(self, connection):
        return 'varchar'

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return json.loads(value)

    def to_python(self, value):
        if isinstance(value, dict):
            return value
        if value is None:
            return value
        return json.loads(value)

    def get_prep_value(self, value):
        return json.dumps(value)


class Drink(models.Model):
    name = models.CharField(max_length=256, null=False)
    color = models.CharField(max_length=7, null=False, default='#FFFFFF')
    creator = models.ForeignKey('users.User', null=True, on_delete=models.CASCADE)
    ingredients = IngredientsField()
    image = models.ImageField(upload_to='images/', default='images/default.jpg')


class Ingredient(models.Model):
    name = models.CharField(max_length=128, null=False, default='Untitled')
    type = models.ForeignKey('IngredientType', on_delete=models.CASCADE)


class IngredientType(models.Model):
    name = models.CharField(max_length=128, null=False, default='Untitled')

    def __unicode__(self):
        return u'{0}'.format(self.name)

    def __str__(self):
        return u'{0}'.format(self.name)