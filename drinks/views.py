import time

from django.core import serializers
from django.http import HttpResponse, HttpResponseBadRequest
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

def drink_new(request):
    drink_form = DrinkForm
    ingredient_type_form = IngredientTypeForm
    ingredient_types = list(map(lambda types: types['name'], IngredientType.objects.values()))

    return render(request, 'drinks/create.html', {
        'drink_form': drink_form,
        'ingredient_type_form': ingredient_type_form,
        'ingredient_types': ingredient_types
    })


def drinks(request, drink_id=None):
    if request.method == "POST":
        form = DrinkForm(request.POST, request.FILES)
        if form.is_valid():
            u = form.save()
            return redirect('/')
        else:
            print("Form is invalid...")
            print(form)
            # TODO: Add error message here
    elif request.method == "GET":
        if drink_id:
            drink_obj = Drink.objects.get(pk=drink_id)
            pumps = Pump.objects.filter(contents__type__name__in=drink_obj.ingredients.keys())
            ingredient_ids = pumps.values_list('contents', flat=True)
            available = Ingredient.objects.filter(id__in=ingredient_ids)
            return render(request, 'drinks/show.html', {
                'drink': drink_obj,
                'available': serializers.serialize('json', available, use_natural_foreign_keys=True)
            })
        else:
           return index(request)


def ingredients(request):
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
    form_class = IngredientForm

    return render(request, 'ingredients/show_ingredients.html')


def ingredient_types(request):
    if request.method == "POST":
        form = IngredientTypeForm(request.POST)
        if form.is_valid():
            u = form.save()
            return HttpResponse(status=204)
        else:
            return HttpResponseBadRequest()
    elif request.method == "GET":
        return HttpResponse(status=204)
    elif request.method == "PUT":
        return HttpResponse(status=204)
    elif request.method == "DELETE":
        return HttpResponse(status=204)
    else:
        print("Unrecognized request method.")


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
        response = requests.get("http://localhost:" + str(settings.WORKER_PORT), params={'drink': json.dumps(simplified), 'color': 'FFFFFF'})
        if response.status_code == 200:
            print(response.text)
        else:
            print("Pour unsuccessful...")
    return HttpResponse("success")
