from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q, Count
from .models import Recipe
from .forms import LoginForm, SignupForm, RecipeSearchForm
import pandas as pd
from io import BytesIO
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

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

def signup_view(request):
    """Handle user registration"""
    error_message = None
    form = SignupForm()
    
    if request.method == 'POST':
        form = SignupForm(data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            
            # Create new user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            
            # Log the user in automatically
            login(request, user)
            
            # Redirect to recipe list
            return redirect('recipes:list')
    
    context = {
        'form': form,
        'error_message': error_message
    }
    return render(request, 'recipes/signup.html', context)

def get_chart(chart_type, data, **kwargs):
    """Generate charts and return as base64 encoded image"""
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(10, 6))
    
    if chart_type == 'bar':
        plt.bar(data['labels'], data['values'])
        plt.xlabel(kwargs.get('xlabel', ''))
        plt.ylabel(kwargs.get('ylabel', ''))
        plt.title(kwargs.get('title', ''))
        plt.xticks(rotation=45, ha='right')
        
    elif chart_type == 'pie':
        plt.pie(data['values'], labels=data['labels'], autopct='%1.1f%%', startangle=90)
        plt.title(kwargs.get('title', ''))
        plt.axis('equal')
        
    elif chart_type == 'line':
        plt.plot(data['labels'], data['values'], marker='o', linewidth=2, markersize=8)
        plt.xlabel(kwargs.get('xlabel', ''))
        plt.ylabel(kwargs.get('ylabel', ''))
        plt.title(kwargs.get('title', ''))
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Convert plot to base64 string
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    
    plt.close()
    
    return graphic

@login_required
def recipe_search(request):
    """Search recipes with filters and optional data visualization"""
    form = RecipeSearchForm(request.GET or None)
    recipes = Recipe.objects.all()
    chart = None
    df = None
    search_performed = False
    
    if request.GET:
        search_performed = True
        
        # Apply filters
        recipe_name = request.GET.get('recipe_name', '').strip()
        ingredient = request.GET.get('ingredient', '').strip()
        difficulty = request.GET.get('difficulty', '').strip()
        cooking_time = request.GET.get('cooking_time', '').strip()
        show_chart = request.GET.get('show_chart', '') == 'on'
        
        # Filter by recipe name (partial match)
        if recipe_name:
            recipes = recipes.filter(name__icontains=recipe_name)
        
        # Filter by ingredient (partial match)
        if ingredient:
            recipes = recipes.filter(ingredients__icontains=ingredient)
        
        # Filter by difficulty
        if difficulty:
            recipes = recipes.filter(difficulty=difficulty)
        
        # Filter by cooking time
        if cooking_time:
            recipes = recipes.filter(cooking_time__lte=int(cooking_time))
        
        # Convert QuerySet to pandas DataFrame
        if recipes.exists():
            recipe_data = []
            for recipe in recipes:
                recipe_data.append({
                    'id': recipe.id,
                    'name': recipe.name,
                    'cooking_time': recipe.cooking_time,
                    'difficulty': recipe.difficulty,
                    'ingredients': len(recipe.get_ingredients_list()),
                })
            df = pd.DataFrame(recipe_data)
            
            # Generate charts if requested
            if show_chart and len(df) > 0:
                charts = []
                
                # Bar Chart - Recipes by Difficulty
                difficulty_counts = df['difficulty'].value_counts()
                bar_data = {
                    'labels': difficulty_counts.index.tolist(),
                    'values': difficulty_counts.values.tolist()
                }
                bar_chart = get_chart(
                    'bar', 
                    bar_data, 
                    title='Recipe Difficulty Distribution',
                    xlabel='Difficulty Level',
                    ylabel='Number of Recipes'
                )
                charts.append(('bar', bar_chart))
                
                # Pie Chart - Cooking Time Distribution
                time_ranges = []
                for time in df['cooking_time']:
                    if time < 10:
                        time_ranges.append('Quick (<10 min)')
                    elif time < 30:
                        time_ranges.append('Medium (10-30 min)')
                    elif time < 60:
                        time_ranges.append('Long (30-60 min)')
                    else:
                        time_ranges.append('Very Long (>60 min)')
                
                time_df = pd.Series(time_ranges).value_counts()
                pie_data = {
                    'labels': time_df.index.tolist(),
                    'values': time_df.values.tolist()
                }
                pie_chart = get_chart(
                    'pie',
                    pie_data,
                    title='Recipes by Cooking Time'
                )
                charts.append(('pie', pie_chart))
                
                # Line Chart - Recipe Collection Growth
                all_recipes = Recipe.objects.all().order_by('created_at')
                if all_recipes.exists():
                    dates = [r.created_at.strftime('%Y-%m-%d') for r in all_recipes]
                    cumulative = list(range(1, len(dates) + 1))
                    
                    # Group by date and get cumulative count
                    date_counts = {}
                    for i, date in enumerate(dates, 1):
                        date_counts[date] = i
                    
                    line_data = {
                        'labels': list(date_counts.keys()),
                        'values': list(date_counts.values())
                    }
                    line_chart = get_chart(
                        'line',
                        line_data,
                        title='Recipe Collection Growth',
                        xlabel='Date Added',
                        ylabel='Total Recipes'
                    )
                    charts.append(('line', line_chart))
                
                chart = charts
    
    context = {
        'form': form,
        'recipes': recipes,
        'df': df.to_html(classes='recipe-table', index=False) if df is not None else None,
        'chart': chart,
        'search_performed': search_performed,
        'recipes_count': recipes.count() if search_performed else 0,
    }
    
    return render(request, 'recipes/recipe_search.html', context)