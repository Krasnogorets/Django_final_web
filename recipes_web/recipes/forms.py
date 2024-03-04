import datetime
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import MultiValueField, CharField, ChoiceField, MultiWidget, TextInput, Select, Textarea,MultipleChoiceField
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from .models import Recipe, Category, Ingredients


class AddNewRecipe(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'cooking_steps', 'category', 'cooking_time',
                  'ingredients', 'picture']
        widgets = {
            'title': TextInput(attrs={'size': 77}),
            'description': Textarea(attrs={'cols': 80, 'rows': 5}),
            'cooking_steps': Textarea(attrs={'cols': 80, 'rows': 7})
        }
