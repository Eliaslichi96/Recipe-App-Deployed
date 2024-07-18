from django.test import TestCase
from django.urls import reverse
from .models import Recipe
from django.contrib.auth.models import User

class RecipeModelTest(TestCase):
    def test_string_representation(self):
        recipe = Recipe(name="Pasta")
        self.assertEqual(str(recipe), recipe.name)

class RecipeViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_recipes = 13
        for recipe_num in range(number_of_recipes):
            Recipe.objects.create(
                name=f"Recipe {recipe_num}",
                ingredients="Ingredient 1, Ingredient 2",
                cooking_time=30,
                description="Test description",
                difficulty="Easy",
                pic="recipes/no_picture"
            )
        
        # Create a user for login
        cls.test_user = User.objects.create_user(username='testuser', password='12345')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('recipes:recipes-list'))
        self.assertRedirects(response, '/login/?next=/recipes/')

    def test_logged_in_uses_correct_template(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('recipes:recipes-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/recipes_list.html')

    def test_pagination_is_ten(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('recipes:recipes-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['object_list']), 10)

    def test_lists_all_recipes(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('recipes:recipes-list') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 3)  # 13 total recipes, 10 on first page, 3 on second page

    def test_recipe_detail_view(self):
        recipe = Recipe.objects.get(id=1)
        response = self.client.get(reverse('recipes:recipe-detail', args=[str(recipe.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, recipe.name)

    def test_recipe_create_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('recipes:recipe-create'), {
            'name': 'New Recipe',
            'ingredients': 'Ingredient 1, Ingredient 2',
            'cooking_time': 30,
            'description': 'Test description',
            'difficulty': 'Easy',
            'pic': 'recipes/no_picture'
        })
        self.assertEqual(response.status_code, 302)  # Redirects after creation
        self.assertEqual(Recipe.objects.last().name, 'New Recipe')

    def test_recipe_update_view(self):
        self.client.login(username='testuser', password='12345')
        recipe = Recipe.objects.get(id=1)
        response = self.client.post(reverse('recipes:recipe-update', args=[str(recipe.id)]), {
            'name': 'Updated Recipe',
            'ingredients': 'Ingredient 1, Ingredient 2',
            'cooking_time': 30,
            'description': 'Updated description',
            'difficulty': 'Easy',
            'pic': 'recipes/no_picture'
        })
        self.assertEqual(response.status_code, 302)  # Redirects after update
        recipe.refresh_from_db()
        self.assertEqual(recipe.name, 'Updated Recipe')
        self.assertEqual(recipe.description, 'Updated description')

    def test_recipe_delete_view(self):
        self.client.login(username='testuser', password='12345')
        recipe = Recipe.objects.get(id=1)
        response = self.client.post(reverse('recipes:recipe-delete', args=[str(recipe.id)]))
        self.assertEqual(response.status_code, 302)  # Redirects after deletion
        self.assertFalse(Recipe.objects.filter(id=1).exists())
