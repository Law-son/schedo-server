from django.urls import path
from . import views

app_name = 'registrations'

urlpatterns = [
    path('attendee/create/', views.create_attendee, name='create_attendee'),
    path('attendees/<int:event_id>/', views.fetch_attendees, name='fetch_attendees'),
    path('ticket/<str:ticket_code>/', views.fetch_ticket, name='fetch_ticket'),
    path('ticket/scan/<str:ticket_code>/', views.scan_ticket, name='scan_ticket'),
]

