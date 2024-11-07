from .models import Event, Archive
from rest_framework import serializers

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id',
            'title',
            'description',
            'location',
            'category',
            'meeting_id',
            'start_date',
            'end_date',
            'start_time',
            'end_time',
            'thumbnail',
            'is_public',
            'is_online',
        ]
        read_only_fields = ['id']

class ArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Archive
        fields = [
            'id',
            'title',
            'description',
            'location',
            'category',
            'meeting_id',
            'start_date',
            'end_date',
            'start_time',
            'end_time',
            'thumbnail',
            'is_public',
            'is_online',
        ]
        read_only_fields = ['id']

