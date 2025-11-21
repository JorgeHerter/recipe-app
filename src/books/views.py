from django.shortcuts import render
from .models import Book

def book_list(request):
    """
    Fetches all books from the database and renders them in a list.
    """
    # Query the database for all Book objects
    books = Book.objects.all().order_by('title')
    
    # Context dictionary holds the data to be passed to the template
    context = {
        'book_list': books
    }
    
    # Render the template, passing the context data
    return render(request, 'book_list.html', context)