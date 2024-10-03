from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'timestamp', 'is_read', 'event']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = instance.user.email
        if instance.event:
            data['event'] = instance.event.title
        else:
            data['event'] = None
        return data
