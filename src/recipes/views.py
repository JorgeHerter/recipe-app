from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Recipe
from .forms import LoginForm

def home(request):
    """Welcome page for the Recipe application"""
    return render(request, 'recipes/recipes_home.html')

def login_view(request):
    """Handle user login"""
    error_message = None
    form = LoginForm()
    
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            # Authenticate user
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # Login successful
                login(request, user)
                # Redirect to recipe list (protected page)
                return redirect('recipes:list')
            else:
                error_message = 'Invalid username or password'
    
    context = {
        'form': form,
        'error_message': error_message
    }
    return render(request, 'recipes/login.html', context)

@login_required
def recipe_list(request):
    """Display all recipes - PROTECTED VIEW"""
    recipes = Recipe.objects.all().order_by('-created_at')
    context = {
        'recipes': recipes
    }
    return render(request, 'recipes/recipe_list.html', context)

@login_required
def recipe_detail(request, pk):
    """Display details for a specific recipe - PROTECTED VIEW"""
    recipe = get_object_or_404(Recipe, pk=pk)
    context = {
        'recipe': recipe,
        'ingredients_list': recipe.get_ingredients_list()
    }
    return render(request, 'recipes/recipe_detail.html', context)

def logout_view(request):
    """Handle user logout"""
    logout(request)
    return render(request, 'recipes/success.html')