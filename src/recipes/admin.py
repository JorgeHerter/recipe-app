from django.contrib import admin
from .models import Ingredient, Recipe, RecipeIngredient

# Inline for managing ingredients within the Recipe admin
class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1  # Allows adding one extra empty form by default

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'difficulty', 'cooking_time')
    search_fields = ('name', 'description')
    inlines = [RecipeIngredientInline]

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)