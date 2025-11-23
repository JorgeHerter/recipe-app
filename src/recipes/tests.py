from django.test import TestCase, Client
from django.urls import reverse
from .models import Recipe

class RecipeModelTest(TestCase):
    """Test Recipe model"""
    
    def setUpTestData():
        """Set up non-modified objects used by all test methods"""
        Recipe.objects.create(
            name='Test Recipe',
            ingredients='ingredient1, ingredient2, ingredient3',
            cooking_time=15,
            description='Test description'
        )
    
    def test_recipe_name(self):
        """Test recipe name field"""
        recipe = Recipe.objects.get(id=1)
        field_label = recipe._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')
    
    def test_recipe_name_max_length(self):
        """Test recipe name max length"""
        recipe = Recipe.objects.get(id=1)
        max_length = recipe._meta.get_field('name').max_length
        self.assertEqual(max_length, 120)
    
    def test_difficulty_calculation_easy(self):
        """Test difficulty calculation for easy recipe"""
        recipe = Recipe.objects.create(
            name='Easy Recipe',
            ingredients='salt, pepper',
            cooking_time=5,
            description='Quick recipe'
        )
        self.assertEqual(recipe.difficulty, 'Easy')
    
    def test_difficulty_calculation_medium(self):
        """Test difficulty calculation for medium recipe"""
        recipe = Recipe.objects.create(
            name='Medium Recipe',
            ingredients='ingredient1, ingredient2, ingredient3, ingredient4',
            cooking_time=8,
            description='Medium complexity'
        )
        self.assertEqual(recipe.difficulty, 'Medium')
    
    def test_difficulty_calculation_intermediate(self):
        """Test difficulty calculation for intermediate recipe"""
        recipe = Recipe.objects.create(
            name='Intermediate Recipe',
            ingredients='ingredient1, ingredient2, ingredient3, ingredient4',
            cooking_time=20,
            description='More complex'
        )
        self.assertEqual(recipe.difficulty, 'Intermediate')
    
    def test_difficulty_calculation_hard(self):
        """Test difficulty calculation for hard recipe"""
        recipe = Recipe.objects.create(
            name='Hard Recipe',
            ingredients='ingredient1, ingredient2, ingredient3, ingredient4, ingredient5',
            cooking_time=45,
            description='Very complex'
        )
        self.assertEqual(recipe.difficulty, 'Hard')
    
    def test_get_ingredients_list(self):
        """Test get_ingredients_list method"""
        recipe = Recipe.objects.get(id=1)
        ingredients = recipe.get_ingredients_list()
        self.assertEqual(len(ingredients), 3)
        self.assertIn('ingredient1', ingredients)
    
    def test_recipe_str_method(self):
        """Test string representation of recipe"""
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(str(recipe), 'Test Recipe')


class RecipeViewsTest(TestCase):
    """Test Recipe views"""
    
    def setUp(self):
        """Set up test client and create test recipes"""
        self.client = Client()
        self.recipe = Recipe.objects.create(
            name='Test Recipe',
            ingredients='ingredient1, ingredient2, ingredient3',
            cooking_time=15,
            description='Test description'
        )
    
    def test_home_view(self):
        """Test home view returns 200"""
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipes_home.html')
    
    def test_recipe_list_view(self):
        """Test recipe list view returns 200 and displays recipes"""
        response = self.client.get(reverse('recipes:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_list.html')
        self.assertContains(response, 'Test Recipe')
    
    def test_recipe_detail_view(self):
        """Test recipe detail view returns 200 and displays correct recipe"""
        response = self.client.get(reverse('recipes:detail', args=[self.recipe.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_detail.html')
        self.assertContains(response, 'Test Recipe')
        self.assertContains(response, 'ingredient1')
    
    def test_recipe_detail_view_invalid_id(self):
        """Test recipe detail view with invalid id returns 404"""
        response = self.client.get(reverse('recipes:detail', args=[9999]))
        self.assertEqual(response.status_code, 404)
    
    def test_recipe_list_links_to_detail(self):
        """Test that recipe list contains links to detail pages"""
        response = self.client.get(reverse('recipes:list'))
        detail_url = reverse('recipes:detail', args=[self.recipe.pk])
        self.assertContains(response, detail_url)
    
    def test_home_links_to_list(self):
        """Test that home page contains link to recipe list"""
        response = self.client.get(reverse('recipes:home'))
        list_url = reverse('recipes:list')
        self.assertContains(response, list_url)


class RecipeURLsTest(TestCase):
    """Test Recipe URLs"""
    
    def test_home_url_resolves(self):
        """Test home URL resolves correctly"""
        url = reverse('recipes:home')
        self.assertEqual(url, '/')
    
    def test_list_url_resolves(self):
        """Test list URL resolves correctly"""
        url = reverse('recipes:list')
        self.assertEqual(url, '/list/')
    
    def test_detail_url_resolves(self):
        """Test detail URL resolves correctly"""
        url = reverse('recipes:detail', args=[1])
        self.assertEqual(url, '/detail/1/')