from django.core import serializers
from django.shortcuts import render, redirect

from drinks.forms import *


def index(request):
    return render(request, 'drinks/index.html', {
        'drinks': Drink.objects.all
    })


def show(request, drink_id):
    return render(request, 'drinks/show.html', {
        'drink': Drink.objects.get(pk=drink_id)
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
