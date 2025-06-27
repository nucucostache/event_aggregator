from django.urls import path
from .views import api_event_list

urlpatterns = [
    path('api-client/', api_event_list, name='api_event_list'),
]
