from django import forms
from django.forms import ModelForm

from recipe.models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('title', 'tag', 'cooking_time', 'description', 'image')
        widgets = {
            'tag': forms.CheckboxSelectMultiple(),
        }
