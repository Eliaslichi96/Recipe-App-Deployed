from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Recipe
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RecipesSearchForm, RecipeForm
import matplotlib.pyplot as plt
import io
import urllib, base64

# Create your views here.
def home_view(request):
    return render(request, 'app/recipes_home.html')

class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = "app/recipes_list.html"
    paginate_by = 10


class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = "app/recipes_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = self.get_object()
        context['ingredients_list'] = recipe.ingredients.split(',')
        return context
    

def records(request):
    form = RecipesSearchForm(request.POST or None)
    recipes = []
    chart = None

    if request.method == 'POST' and form.is_valid():
        recipe_name = form.cleaned_data['recipe_name']
        chart_type = form.cleaned_data['chart_type']
        recipes = Recipe.objects.filter(name__icontains=recipe_name)

        if chart_type == '#1':
            chart = generate_bar_chart(recipes)
        elif chart_type == '#2':
            chart = generate_pie_chart(recipes)
        elif chart_type == '#3':
            chart = generate_line_chart(recipes)

    context = {
        'form': form,
        'recipes': recipes,
        'chart': chart,
    }

    return render(request, 'app/recipes_records.html', context)

def generate_bar_chart(recipes):
    names = [recipe.name for recipe in recipes]
    times = [recipe.cooking_time for recipe in recipes]
    plt.figure()
    plt.bar(names, times)
    plt.xlabel('Recipe Name')
    plt.ylabel('Cooking Time')
    plt.title('Bar Chart of Cooking Times')
    return get_chart()

def generate_pie_chart(recipes):
    names = [recipe.name for recipe in recipes]
    times = [recipe.cooking_time for recipe in recipes]
    plt.figure()
    plt.pie(times, labels=names, autopct='%1.1f%%')
    plt.title('Pie Chart of Cooking Times')
    return get_chart()

def generate_line_chart(recipes):
    names = [recipe.name for recipe in recipes]
    times = [recipe.cooking_time for recipe in recipes]
    plt.figure()
    plt.plot(names, times, marker='o')
    plt.xlabel('Recipe Name')
    plt.ylabel('Cooking Time')
    plt.title('Line Chart of Cooking Times')
    return get_chart()

def get_chart():
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return uri

def recipe_create_view(request):
    form = RecipeForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('recipes:recipes-list')
    return render(request, 'app/recipe_form.html', {'form': form})

def recipe_edit_view(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    form = RecipeForm(request.POST or None, request.FILES or None, instance=recipe)
    if form.is_valid():
        form.save()
        return redirect('recipes:detail', pk=pk)
    return render(request, 'app/recipe_form.html', {'form': form})