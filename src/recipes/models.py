from django.db import models

class Recipe(models.Model):
    name = models.CharField(max_length=120)
    ingredients = models.TextField(help_text="Enter ingredients separated by commas")
    cooking_time = models.IntegerField(help_text="Cooking time in minutes")
    difficulty = models.CharField(max_length=20, blank=True, editable=False)
    description = models.TextField(default='', help_text="Cooking instructions")
    pic = models.ImageField(upload_to='recipes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def calculate_difficulty(self):
        """Calculate recipe difficulty based on cooking time and number of ingredients"""
        num_ingredients = len([i.strip() for i in self.ingredients.split(',') if i.strip()])
        
        if self.cooking_time < 10 and num_ingredients < 4:
            return 'Easy'
        elif self.cooking_time < 10 and num_ingredients >= 4:
            return 'Medium'
        elif self.cooking_time >= 10 and num_ingredients < 4:
            return 'Medium'
        elif self.cooking_time >= 10 and num_ingredients >= 4 and self.cooking_time < 30:
            return 'Intermediate'
        else:
            return 'Hard'
    
    def save(self, *args, **kwargs):
        """Override save to automatically calculate difficulty"""
        self.difficulty = self.calculate_difficulty()
        super().save(*args, **kwargs)
    
    def get_ingredients_list(self):
        """Return ingredients as a list"""
        return [i.strip() for i in self.ingredients.split(',') if i.strip()]