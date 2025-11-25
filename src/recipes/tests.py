from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Recipe
from .forms import LoginForm, SignupForm, RecipeSearchForm

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


class RecipeFormTest(TestCase):
    """Test Recipe forms"""
    
    def test_login_form_valid(self):
        """Test login form with valid data"""
        form = LoginForm(data={
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertTrue(form.is_valid())
    
    def test_login_form_empty(self):
        """Test login form with empty data"""
        form = LoginForm(data={})
        self.assertFalse(form.is_valid())
    
    def test_signup_form_valid(self):
        """Test signup form with valid data"""
        form = SignupForm(data={
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        })
        self.assertTrue(form.is_valid())
    
    def test_signup_form_passwords_dont_match(self):
        """Test signup form with mismatched passwords"""
        form = SignupForm(data={
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password1': 'testpass123',
            'password2': 'different123'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('Passwords do not match', str(form.errors))
    
    def test_signup_form_duplicate_username(self):
        """Test signup form with existing username"""
        # Create a user first
        User.objects.create_user(username='existinguser', password='pass123')
        
        # Try to create another user with same username
        form = SignupForm(data={
            'username': 'existinguser',
            'email': 'new@test.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
    
    def test_signup_form_email_optional(self):
        """Test signup form with no email (should be valid)"""
        form = SignupForm(data={
            'username': 'newuser',
            'password1': 'testpass123',
            'password2': 'testpass123'
        })
        self.assertTrue(form.is_valid())
    
    def test_search_form_all_fields(self):
        """Test search form with all fields filled"""
        form = RecipeSearchForm(data={
            'recipe_name': 'Pasta',
            'ingredient': 'tomato',
            'difficulty': 'Easy',
            'cooking_time': '30',
            'show_chart': True
        })
        self.assertTrue(form.is_valid())
    
    def test_search_form_empty(self):
        """Test search form with no data (should be valid as all fields optional)"""
        form = RecipeSearchForm(data={})
        self.assertTrue(form.is_valid())
    
    def test_search_form_partial_data(self):
        """Test search form with only some fields"""
        form = RecipeSearchForm(data={
            'recipe_name': 'Pasta',
            'difficulty': 'Medium'
        })
        self.assertTrue(form.is_valid())
    
    def test_search_form_fields_not_required(self):
        """Test that search form fields are not required"""
        form = RecipeSearchForm()
        self.assertFalse(form.fields['recipe_name'].required)
        self.assertFalse(form.fields['ingredient'].required)
        self.assertFalse(form.fields['difficulty'].required)
        self.assertFalse(form.fields['cooking_time'].required)


class RecipeViewsTest(TestCase):
    """Test Recipe views"""
    
    def setUp(self):
        """Set up test client, user, and create test recipes"""
        self.client = Client()
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123'
        )
        # Create test recipes
        self.recipe1 = Recipe.objects.create(
            name='Pasta Carbonara',
            ingredients='pasta, eggs, bacon, cheese',
            cooking_time=20,
            description='Delicious pasta'
        )
        self.recipe2 = Recipe.objects.create(
            name='Chicken Soup',
            ingredients='chicken, carrots, onions',
            cooking_time=45,
            description='Hearty soup'
        )
        self.recipe3 = Recipe.objects.create(
            name='Quick Salad',
            ingredients='lettuce, tomato',
            cooking_time=5,
            description='Easy salad'
        )
    
    def test_home_view(self):
        """Test home view returns 200"""
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipes_home.html')
    
    def test_login_view_get(self):
        """Test login view GET request returns 200"""
        response = self.client.get(reverse('recipes:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/login.html')
    
    def test_login_view_post_success(self):
        """Test successful login"""
        response = self.client.post(reverse('recipes:login'), {
            'username': 'testuser',
            'password': 'testpassword123'
        })
        # Should redirect to recipe list after successful login
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('recipes:list'))
    
    def test_login_view_post_failure(self):
        """Test failed login with wrong credentials"""
        response = self.client.post(reverse('recipes:login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        # Should stay on login page
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password')
    
    def test_recipe_list_view_authenticated(self):
        """Test recipe list view when logged in"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('recipes:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_list.html')
        self.assertContains(response, 'Pasta Carbonara')
    
    def test_recipe_list_view_not_authenticated(self):
        """Test recipe list view redirects when not logged in"""
        response = self.client.get(reverse('recipes:list'))
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)
    
    def test_recipe_detail_view_authenticated(self):
        """Test recipe detail view when logged in"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('recipes:detail', args=[self.recipe1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_detail.html')
        self.assertContains(response, 'Pasta Carbonara')
        self.assertContains(response, 'pasta')
    
    def test_recipe_detail_view_not_authenticated(self):
        """Test recipe detail view redirects when not logged in"""
        response = self.client.get(reverse('recipes:detail', args=[self.recipe1.pk]))
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)
    
    def test_recipe_detail_view_invalid_id(self):
        """Test recipe detail view with invalid id returns 404"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('recipes:detail', args=[9999]))
        self.assertEqual(response.status_code, 404)
    
    def test_logout_view(self):
        """Test logout view"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('recipes:logout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/success.html')
    
    def test_signup_view_get(self):
        """Test signup view GET request returns 200"""
        response = self.client.get(reverse('recipes:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/signup.html')
    
    def test_signup_view_post_success(self):
        """Test successful signup"""
        response = self.client.post(reverse('recipes:signup'), {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        })
        # Should redirect to recipe list after successful signup
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('recipes:list'))
        # Verify user was created
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_signup_view_post_failure_passwords_dont_match(self):
        """Test signup with mismatched passwords"""
        response = self.client.post(reverse('recipes:signup'), {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password1': 'testpass123',
            'password2': 'different123'
        })
        # Should stay on signup page
        self.assertEqual(response.status_code, 200)
        # User should not be created
        self.assertFalse(User.objects.filter(username='newuser').exists())
    
    def test_signup_view_post_failure_duplicate_username(self):
        """Test signup with existing username"""
        response = self.client.post(reverse('recipes:signup'), {
            'username': 'testuser',  # This user already exists from setUp
            'email': 'another@test.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        })
        # Should stay on signup page
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'already taken')
    
    def test_signup_automatically_logs_in_user(self):
        """Test that signup automatically logs in the new user"""
        response = self.client.post(reverse('recipes:signup'), {
            'username': 'autouser',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }, follow=True)
        # User should be logged in
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertEqual(response.context['user'].username, 'autouser')
    
    def test_recipe_search_view_authenticated(self):
        """Test recipe search view when logged in"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_search.html')
    
    def test_recipe_search_view_not_authenticated(self):
        """Test recipe search view redirects when not logged in"""
        response = self.client.get(reverse('recipes:search'))
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)
    
    def test_recipe_search_by_name(self):
        """Test searching recipes by name"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('recipes:search'), {'recipe_name': 'pasta'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pasta Carbonara')
        self.assertNotContains(response, 'Chicken Soup')
    
    def test_recipe_search_by_ingredient(self):
        """Test searching recipes by ingredient"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('recipes:search'), {'ingredient': 'chicken'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Chicken Soup')
        self.assertNotContains(response, 'Pasta Carbonara')
    
    def test_recipe_search_by_difficulty(self):
        """Test searching recipes by difficulty"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('recipes:search'), {'difficulty': 'Easy'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Quick Salad')
    
    def test_recipe_search_by_cooking_time(self):
        """Test searching recipes by cooking time"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('recipes:search'), {'cooking_time': '10'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Quick Salad')
        self.assertNotContains(response, 'Pasta Carbonara')
    
    def test_recipe_search_partial_match(self):
        """Test searching with partial text match"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('recipes:search'), {'recipe_name': 'chick'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Chicken Soup')
    
    def test_recipe_search_case_insensitive(self):
        """Test searching is case insensitive"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('recipes:search'), {'recipe_name': 'PASTA'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Pasta Carbonara')
    
    def test_recipe_search_results_clickable(self):
        """Test that search results contain clickable links"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('recipes:search'), {'recipe_name': 'pasta'})
        detail_url = reverse('recipes:detail', args=[self.recipe1.pk])
        self.assertContains(response, detail_url)


class RecipeURLsTest(TestCase):
    """Test Recipe URLs"""
    
    def test_home_url_resolves(self):
        """Test home URL resolves correctly"""
        url = reverse('recipes:home')
        self.assertEqual(url, '/')
    
    def test_login_url_resolves(self):
        """Test login URL resolves correctly"""
        url = reverse('recipes:login')
        self.assertEqual(url, '/login/')
    
    def test_logout_url_resolves(self):
        """Test logout URL resolves correctly"""
        url = reverse('recipes:logout')
        self.assertEqual(url, '/logout/')
    
    def test_signup_url_resolves(self):
        """Test signup URL resolves correctly"""
        url = reverse('recipes:signup')
        self.assertEqual(url, '/signup/')
    
    def test_list_url_resolves(self):
        """Test list URL resolves correctly"""
        url = reverse('recipes:list')
        self.assertEqual(url, '/list/')
    
    def test_search_url_resolves(self):
        """Test search URL resolves correctly"""
        url = reverse('recipes:search')
        self.assertEqual(url, '/search/')
    
    def test_detail_url_resolves(self):
        """Test detail URL resolves correctly"""
        url = reverse('recipes:detail', args=[1])
        self.assertEqual(url, '/detail/1/')

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
        """Set up test client, user, and create test recipes"""
        self.client = Client()
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123'
        )
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
    
    def test_login_view_get(self):
        """Test login view GET request returns 200"""
        response = self.client.get(reverse('recipes:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/login.html')
    
    def test_login_view_post_success(self):
        """Test successful login"""
        response = self.client.post(reverse('recipes:login'), {
            'username': 'testuser',
            'password': 'testpassword123'
        })
        # Should redirect to recipe list after successful login
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('recipes:list'))
    
    def test_login_view_post_failure(self):
        """Test failed login with wrong credentials"""
        response = self.client.post(reverse('recipes:login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        # Should stay on login page
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password')
    
    def test_recipe_list_view_authenticated(self):
        """Test recipe list view when logged in"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('recipes:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_list.html')
        self.assertContains(response, 'Test Recipe')
    
    def test_recipe_list_view_not_authenticated(self):
        """Test recipe list view redirects when not logged in"""
        response = self.client.get(reverse('recipes:list'))
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)
    
    def test_recipe_detail_view_authenticated(self):
        """Test recipe detail view when logged in"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('recipes:detail', args=[self.recipe.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_detail.html')
        self.assertContains(response, 'Test Recipe')
        self.assertContains(response, 'ingredient1')
    
    def test_recipe_detail_view_not_authenticated(self):
        """Test recipe detail view redirects when not logged in"""
        response = self.client.get(reverse('recipes:detail', args=[self.recipe.pk]))
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)
    
    def test_recipe_detail_view_invalid_id(self):
        """Test recipe detail view with invalid id returns 404"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('recipes:detail', args=[9999]))
        self.assertEqual(response.status_code, 404)
    
    def test_logout_view(self):
        """Test logout view"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('recipes:logout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/success.html')
    
    def test_recipe_list_has_logout_link_when_authenticated(self):
        """Test that recipe list has logout link when user is logged in"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('recipes:list'))
        self.assertContains(response, 'Logout')


class RecipeURLsTest(TestCase):
    """Test Recipe URLs"""
    
    def test_home_url_resolves(self):
        """Test home URL resolves correctly"""
        url = reverse('recipes:home')
        self.assertEqual(url, '/')
    
    def test_login_url_resolves(self):
        """Test login URL resolves correctly"""
        url = reverse('recipes:login')
        self.assertEqual(url, '/login/')
    
    def test_logout_url_resolves(self):
        """Test logout URL resolves correctly"""
        url = reverse('recipes:logout')
        self.assertEqual(url, '/logout/')
    
    def test_list_url_resolves(self):
        """Test list URL resolves correctly"""
        url = reverse('recipes:list')
        self.assertEqual(url, '/list/')
    
    def test_detail_url_resolves(self):
        """Test detail URL resolves correctly"""
        url = reverse('recipes:detail', args=[1])
        self.assertEqual(url, '/detail/1/')