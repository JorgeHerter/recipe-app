from django.db import models

# Define the Recipe model
class Recipe(models.Model):
    """
    Represents a single recipe entry in the database.
    """
    
    # Text field for the title of the recipe (e.g., "Classic Lasagna")
    # max_length is required for CharField.
    title = models.CharField(max_length=200)
    
    # Large text field for the detailed instructions or description
    description = models.TextField()
    
    # Text field for listing the ingredients. We'll use a large text field 
    # to allow multi-line input and formatting by the user.
    ingredients = models.TextField()
    
    # Automatically records the date and time when the recipe was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # Optional: Field to track the last time the recipe was modified.
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Returns a string representation of the model object (useful for the Django Admin).
        """
        return self.title

    class Meta:
        """
        Meta class options for the model.
        """
        # Orders the recipes by creation date, newest first.
        ordering = ['-created_at'] 
        # Makes the model name plural in the Admin interface look nicer
        verbose_name_plural = "Recipes"