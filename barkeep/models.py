from django.db import models


class Pump(models.Model):
    address = models.PositiveSmallIntegerField()
    contents = models.ForeignKey('drinks.Ingredient', on_delete=models.CASCADE, null=True, blank=True)


