from django.contrib import admin
from .models import Book # This import should now work!

# Register your models here.
admin.site.register(Book)