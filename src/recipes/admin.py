from django.contrib import admin
from .models import Recipe

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'cooking_time', 'difficulty', 'created_at')
    list_filter = ('difficulty', 'created_at')
    search_fields = ('name', 'ingredients', 'description')
    readonly_fields = ('difficulty', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'pic')
        }),
        ('Recipe Details', {
            'fields': ('ingredients', 'cooking_time', 'description')
        }),
        ('Auto-calculated', {
            'fields': ('difficulty',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )