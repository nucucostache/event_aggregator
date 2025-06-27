# users/urls.py
from django.urls import path
from .views import register, login_view  # importă view-urile corecte
from . import views

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

]
