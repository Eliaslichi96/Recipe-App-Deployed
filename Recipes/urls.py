from django.urls import path
from .views import home_view, RecipeListView, RecipeDetailView, records,  recipe_create_view, recipe_edit_view

app_name = 'recipes'  

urlpatterns = [
    path('', home_view, name='home'),
    path('recipes/', RecipeListView.as_view(), name='recipes-list'),
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='detail'),
    path('records/', records, name='records'),
    path('recipes/create/', recipe_create_view, name='recipe-create'),
    path('recipes/<int:pk>/edit/', recipe_edit_view, name='recipe-edit'),
]
