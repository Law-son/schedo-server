from rest_framework import serializers
from .models import Attendee, Ticket

class AttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'gender', 'event', 'registration_date', 'status']
        read_only_fields = ['id', 'registration_date', 'status']

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'event', 'attendee', 'event_title', 'first_name', 'last_name', 'ticket_code', 'issued_date', 'is_used', 'created_by']
        read_only_fields = ['id', 'issued_date']

