from django.urls import path, include
from . import views

# Set the application namespace
app_name = 'books'

# Define URL patterns for the books app
urlpatterns = [
    # Path for the main book list page: /books/
    path('', views.book_list, name='book_list'),

    path('books/', include('books.urls')),
]