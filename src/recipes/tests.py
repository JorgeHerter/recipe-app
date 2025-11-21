from django.test import TestCase
from .models import Ingredient, Recipe, RecipeIngredient

# --- Test Ingredient Model ---
class IngredientModelTest(TestCase):
    def setUp(self):
        self.ingredient = Ingredient.objects.create(name='Flour')

    def test_ingredient_creation(self):
        self.assertTrue(isinstance(self.ingredient, Ingredient))
        self.assertEqual(self.ingredient.name, 'Flour')

    def test_ingredient_str(self):
        self.assertEqual(str(self.ingredient), 'Flour')


# --- Test Recipe Model ---
class RecipeModelTest(TestCase):
    def setUp(self):
        # Create an ingredient first
        self.flour = Ingredient.objects.create(name='Flour')

        # Create a recipe
        self.recipe = Recipe.objects.create(
            name='Simple Bread',
            description='A basic bread recipe.',
            cooking_time=60,
            difficulty='Easy'
        )
        
    def test_recipe_creation(self):
        self.assertTrue(isinstance(self.recipe, Recipe))
        self.assertEqual(self.recipe.name, 'Simple Bread')
        self.assertEqual(self.recipe.difficulty, 'Easy')
        
    def test_recipe_str(self):
        self.assertEqual(str(self.recipe), 'Simple Bread')

    def test_difficulty_choices(self):
        # Test a valid choice
        Recipe.objects.create(name='Hard Stew', description='', cooking_time=120, difficulty='Hard')
        self.assertEqual(Recipe.objects.get(name='Hard Stew').difficulty, 'Hard')


# --- Test RecipeIngredient Model and Relationship ---
class RecipeIngredientModelTest(TestCase):
    def setUp(self):
        self.recipe = Recipe.objects.create(
            name='Pancakes', description='Fluffy pancakes.', cooking_time=30, difficulty='Medium'
        )
        self.ingredient_a = Ingredient.objects.create(name='Milk')
        self.ingredient_b = Ingredient.objects.create(name='Egg')
        
        # Create the intermediary object
        self.recipe_ingredient = RecipeIngredient.objects.create(
            recipe=self.recipe,
            ingredient=self.ingredient_a,
            amount=250.5,
            unit='ml'
        )

    def test_recipe_ingredient_creation(self):
        self.assertTrue(isinstance(self.recipe_ingredient, RecipeIngredient))
        self.assertEqual(self.recipe_ingredient.amount, 250.5)
        self.assertEqual(self.recipe_ingredient.unit, 'ml')
        self.assertEqual(self.recipe_ingredient.recipe.name, 'Pancakes')
        self.assertEqual(self.recipe_ingredient.ingredient.name, 'Milk')

    def test_recipe_ingredient_str(self):
        expected_str = '250.50 ml of Milk in Pancakes'
        self.assertEqual(str(self.recipe_ingredient), expected_str)

    def test_many_to_many_relationship(self):
        # Add a second ingredient through the intermediary model
        RecipeIngredient.objects.create(
            recipe=self.recipe,
            ingredient=self.ingredient_b,
            amount=2,
            unit='units'
        )
        
        # Check that the recipe now lists both ingredients
        ingredients_names = [i.name for i in self.recipe.ingredients.all()]
        self.assertIn('Milk', ingredients_names)
        self.assertIn('Egg', ingredients_names)
        self.assertEqual(self.recipe.ingredients.count(), 2)