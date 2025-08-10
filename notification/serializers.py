from rest_framework import serializers
from notification.models import InAppNotification


class InAppNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InAppNotification
        fields = ['id', 'notification', 'created_at', 'read_at', 'status']
        read_only_fields = ['created_at']