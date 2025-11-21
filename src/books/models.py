from django.db import models

class Book(models.Model):
    """
    A simple model representing a Book, used to resolve the ImportError.
    """
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    
    def __str__(self):
        return self.title