from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('list/', views.recipe_list, name='list'),
    path('detail/<int:pk>/', views.recipe_detail, name='detail'),
]