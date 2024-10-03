from rest_framework import serializers
from .models import Attendee, Ticket

class AttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = ['id', 'user', 'event', 'registration_date', 'status']

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'event', 'first_name', 'last_name', 'issued_date', 'is_used']
