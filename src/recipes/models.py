from django.db import models

class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name


class Recipe(models.Model):
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    cooking_time = models.IntegerField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='Medium')
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    
    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.FloatField(default=1.0)  # Add default here
    unit = models.CharField(max_length=50, default='unit')  # Add default here
    
    def __str__(self):
        return f"{self.amount:.2f} {self.unit} of {self.ingredient.name} in {self.recipe.name}"