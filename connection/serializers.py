from rest_framework import serializers
from connection.choices import RequestStatus
from connection.models import ConnectionRequest
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()


class ConnectionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectionRequest
        fields = ['id', 'sender', 'receiver', 'status', 'created_at']
        read_only_fields = ['status', 'created_at', 'sender']

    def validate_receiver(self, value):
        """
        Ensure that the receiver is not the same as the sender.
        Also ensure there is no existing pending connection request between the users.
        """        
        sender = self.context['request'].user

        if value == sender:
            raise serializers.ValidationError("You cannot send a connection request to yourself.")

        exists = ConnectionRequest.objects.filter(
            Q(sender=sender, receiver=value)
        ).exists()

        if exists:
            raise serializers.ValidationError("A connection request already exists.")

        return value
    

class RequestStatusSerializer(serializers.Serializer):
    """
    Serializer for validating the status of a connection request.
    """
    status = serializers.ChoiceField(
        choices=[(choice, choice) for choice in RequestStatus.choices],
        required=True
    )

    def validate_status(self, value):
        if value not in [RequestStatus.ACCEPTED, RequestStatus.REJECTED]:
            raise serializers.ValidationError("Invalid status.")
        return value 
