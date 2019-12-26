from django.forms import ModelForm, ModelChoiceField, CharField, TextInput, ImageField, ClearableFileInput
from drinks.models import *


class DrinkForm(ModelForm):
    color = CharField(max_length=7, widget=TextInput(attrs={'id': 'colorPicker', 'class': 'basic'}))
    name = CharField(max_length=64, widget=TextInput(attrs={'placeholder': 'Name', 'class': 'col-8 offset-2 col-sm-6 offset-sm-3 form-control' }))
    image = ImageField(widget=ClearableFileInput(attrs={'style': 'display: none'}))

    class Meta:
        model = Drink
        exclude = ['creator', 'ingredients']


class IngredientForm(ModelForm):
    type = ModelChoiceField(queryset=IngredientType.objects, empty_label=None, to_field_name='name')

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientTypeForm(ModelForm):
    class Meta:
        model = IngredientType
        fields = '__all__'
