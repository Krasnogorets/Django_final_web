from django import forms
from django.forms import TextInput, Textarea

from .models import Recipe
from django.utils.translation import gettext as _


class AddNewRecipe(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'cooking_steps', 'category', 'cooking_time',
                  'ingredients', 'picture']
        widgets = {
            'title': TextInput(attrs={'size': 77}),
            'description': Textarea(attrs={'cols': 80, 'rows': 5}),
            'cooking_steps': Textarea(attrs={'cols': 80, 'rows': 7})}
        _


#
class RecipeSearchForm(forms.Form):
    query = forms.CharField(label='Поиск по тексту', max_length=200, empty_value="", required=False,
                            widget=forms.TextInput(attrs={"style": "width: 400px;"}))
