from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from connection.choices import RequestStatus

User = get_user_model()


class ConnectionRequest(models.Model):
    sender = models.ForeignKey(
        User,
        related_name='connection_requests_sent',
        on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        User,
        related_name='connection_requests_received',
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=10,
        choices=RequestStatus.choices,
        default=RequestStatus.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('sender', 'receiver')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.sender} -> {self.receiver} ({self.status})"


class Connection(models.Model):
    participant_one = models.ForeignKey(
        User,
        related_name='connections_participant_one',
        on_delete=models.CASCADE
    )
    participant_two = models.ForeignKey(
        User,
        related_name='connections_participant_two',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('participant_one', 'participant_two')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.participant_one} <--> {self.participant_two}"
