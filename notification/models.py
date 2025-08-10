from django.db import models
from django.contrib.auth import get_user_model
from notification.choices import EmailNotificationStatus, InAppNotificationStatus, NotificationType

User = get_user_model()


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=100, null=False, blank=False)
    body = models.TextField(null=True, blank=True)
    notification_type = models.CharField(
        max_length=20, choices=NotificationType.choices,
        default=NotificationType.CONNECTION_REQUEST
    )


class InAppNotification(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='in_app_notifications')
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(
        choices=InAppNotificationStatus.choices,
        default=InAppNotificationStatus.UNREAD
    )


class EmailNotification(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='email_notifications')
    delivered_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    error_message = models.TextField(blank=True, null=True)
    status = models.CharField(
        choices=EmailNotificationStatus.choices,
        default=EmailNotificationStatus.PENDING
    )
