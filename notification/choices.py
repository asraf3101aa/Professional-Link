from django.db import models
from django.utils.translation import gettext_lazy as _


class NotificationType(models.TextChoices):
    CONNECTION_REQUEST = 'connection_request',  _('Connection Request')


class EmailNotificationStatus(models.TextChoices):
    PENDING = 'pending',  _('Pending')
    SENT = 'sent', _('Sent')
    FAILED = 'failed', _('Failed')


class InAppNotificationStatus(models.TextChoices):
    UNREAD = 'unread', _('Unread')
    READ = 'read', _('Read')