import time

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
from sphinx.util import requests

from bartender.models import Settings
from drinks.forms import *
from barkeep.models import Pump

import json


def index(request):
    return render(request, 'drinks/index.html', {
        'drinks': Drink.objects.all
    })


def show(request, drink_id):
    drink = Drink.objects.get(pk=drink_id)
    pumps = Pump.objects.filter(contents__type__name__in=drink.ingredients.keys())
    ingredient_ids = pumps.values_list('contents', flat=True)
    available = Ingredient.objects.filter(id__in=ingredient_ids)
    return render(request, 'drinks/show.html', {
        'drink': drink,
        'available': serializers.serialize('json', available, use_natural_foreign_keys=True)
    })


def create(request):
    if request.method == "POST":
        form = DrinkForm(request.POST, request.FILES)
        if form.is_valid():
            u = form.save()
            return redirect('/')
        else:
            form_class = DrinkForm
            print("Form is invalid...")
            print(form)
            # TODO: Add error message here
    else:
        form_class = DrinkForm

    ing = list(map(lambda ing: ing['name'], IngredientType.objects.values()))

    return render(request, 'drinks/create.html', {
        'form': form_class,
        'ingredients': ing
    })


def ingredients(request):
    form_class = IngredientForm

    return render(request, 'ingredients/show_ingredients.html')


def new_ingredient(request):
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            u = form.save()
            print(form)
            return render(request, 'ingredients/show_ingredients.html')
    else:
        form_class = IngredientForm

    return render(request, 'ingredients/create_ingredient.html', {
        'form': form_class
    })


def pour(request):
    if request.method == "POST":
        drink_json = request.POST.get('drink')
        drink = json.loads(drink_json)
        pumps = Pump.objects.filter(contents__name__in=drink)
        simplified = {}
        for pump in pumps:
            pour_time = Settings.objects.first().oz_interval * drink[pump.contents.name]
            simplified[str(pump.address)] = pour_time
        print(simplified)
        response = requests.get("http://localhost:" + str(settings.WORKER_PORT), params={'drink': json.dumps(simplified)})
        if response.status_code == 200:
            print(time.localtime(int(response.text)/1000))
        else:
            print("Pour unsuccessful...")
    return HttpResponse("success")
