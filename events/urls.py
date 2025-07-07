from django.urls import path
from . import views

from .views import upcoming_events_api

app_name = 'events'

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('dashboard/', views.organizer_dashboard, name='dashboard_organizator'),
    path('user-dashboard/', views.user_dashboard, name='dashboard_user'),    
    path('event/add/', views.add_event, name='add_event'),
    path('event/<int:event_id>/edit/', views.edit_event, name='edit_event'),
    path('event/<int:event_id>/delete/', views.delete_event, name='delete_event'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('event/<int:event_id>/register/', views.register_for_event, name='register_for_event'),
    path('event/<int:event_id>/unregister/', views.unregister_from_event, name='unregister_from_event'),
    path('my-events/', views.my_events, name='my_events'),
    

]

urlpatterns += [
    path('api/upcoming/', upcoming_events_api, name='upcoming_events_api'),
]
