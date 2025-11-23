from django.shortcuts import render, get_object_or_404
from .models import Recipe

def home(request):
    """Welcome page for the Recipe application"""
    return render(request, 'recipes/recipes_home.html')

def recipe_list(request):
    """Display all recipes"""
    recipes = Recipe.objects.all().order_by('-created_at')
    context = {
        'recipes': recipes
    }
    return render(request, 'recipes/recipe_list.html', context)

def recipe_detail(request, pk):
    """Display details for a specific recipe"""
    recipe = get_object_or_404(Recipe, pk=pk)
    context = {
        'recipe': recipe,
        'ingredients_list': recipe.get_ingredients_list()
    }
    return render(request, 'recipes/recipe_detail.html', context)