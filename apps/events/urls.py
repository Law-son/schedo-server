from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('public/', views.get_public_events, name='public_events'),
    path('user/', views.get_user_events, name='user_events'),
    path('event/<int:event_id>/', views.get_event, name='event'),
    path('create/', views.create_event, name='creat_event'),
    path('update/<int:event_id>/', views.update_event, name='update_event'),
    path('delete/<int:event_id>/', views.delete_event, name='delete_event'),
]

