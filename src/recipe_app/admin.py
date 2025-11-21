from django.contrib import admin
from .models import Recipe

# Register the Recipe model so it appears in the Django Admin interface.
admin.site.register(Recipe)