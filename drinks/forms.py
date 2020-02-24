from django.forms import ModelForm, ModelChoiceField, CharField, TextInput, ImageField, ClearableFileInput, HiddenInput
from drinks.models import *


class DrinkForm(ModelForm):
    color = CharField(max_length=7, widget=TextInput(attrs={'id': 'colorPicker', 'class': 'basic'}))
    name = CharField(max_length=64, widget=TextInput(attrs={'placeholder': 'Name', 'class': 'col-8 offset-2 col-sm-6 offset-sm-3 form-control' }))
    image = ImageField(required=False, widget=ClearableFileInput(attrs={'style': 'display: none'}))
    ingredients = CharField(max_length=1024, widget=HiddenInput())

    class Meta:
        model = Drink
        exclude = ['creator']


class IngredientForm(ModelForm):
    type = ModelChoiceField(queryset=IngredientType.objects, empty_label=None, to_field_name='name')
    name = CharField(max_length=128, widget=TextInput(attrs={'placeholder': 'Name', 'class': 'col-8 offset-2 col-sm-6 offset-sm-3 form-control' }))

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientTypeForm(ModelForm):
    name = CharField(max_length=128, widget=TextInput(attrs={'placeholder': 'Name', 'class': 'col-8 offset-2 col-sm-6 offset-sm-3 form-control' }))

    class Meta:
        model = IngredientType
        fields = '__all__'
