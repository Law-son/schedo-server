from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('public/', views.get_public_events, name='public_events'),
    path('user/', views.get_user_events, name='user_events'),
    path('archives/', views.get_user_archives, name='user_archives'),
    path('event/<int:event_id>/', views.get_event, name='event'),
    path('attendance/', views.get_event_attendance, name='event_attendance'),
    path('create/', views.create_event, name='creat_event'),
    path('update/<int:event_id>/', views.update_event, name='update_event'),
    path('archive/<int:event_id>/', views.archive_event, name='archive_event'),
    path('delete/all/', views.delete_all_events, name='delete_all_events'),
    path('restore/all/', views.restore_all_events, name='restore_all_events'),
    path('delete/<int:event_id>/', views.delete_event, name='delete_event'),
    path('restore/<int:event_id>/', views.restore_event, name='delete_event'),
]
