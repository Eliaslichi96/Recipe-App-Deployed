from django import forms    #import django forms
from .models import Recipe


CHART__CHOICES = (          #specify choices as a tuple
   ('#1', 'Bar chart'),    # when user selects "Bar chart", it is stored as "#1"
   ('#2', 'Pie chart'),
   ('#3', 'Line chart')
   )
#define class-based Form imported from Django forms
class RecipesSearchForm(forms.Form):
    recipe_name = forms.CharField(max_length=100)
    chart_type = forms.ChoiceField(choices=CHART__CHOICES)

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'ingredients', 'cooking_time', 'description', 'difficulty', 'pic']

