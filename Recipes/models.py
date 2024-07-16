from django.db import models
from django.urls import reverse

# Create your models here.

class Recipe(models.Model):
    name = models.CharField(max_length=100)
    ingredients = models.TextField()
    cooking_time = models.IntegerField()
    description = models.TextField()
    difficulty = models.CharField(max_length=50)
    pic = models.ImageField(upload_to="recipes", default="no_picture")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("recipes:detail", kwargs={"pk": self.pk})
