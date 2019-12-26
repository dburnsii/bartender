from django.db import models


class Pump(models.Model):
    location = models.PositiveSmallIntegerField()
    address = models.PositiveSmallIntegerField()
    contents = models.ForeignKey('drinks.Ingredient', on_delete=models.CASCADE)


