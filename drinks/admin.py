from django.contrib import admin

from drinks.models import *

admin.site.register(Drink)
admin.site.register(Ingredient)
admin.site.register(IngredientType)
