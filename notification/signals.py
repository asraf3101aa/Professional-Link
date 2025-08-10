import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from notification.models import InAppNotification, Notification
from notification.tasks import send_email_notification

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Notification)
def send_notification(sender, instance, created, **kwargs):
    """
    Trigger sending both email and in-app notifications when a Notification is created.
    """
    if not created:
        return 

    logger.info(f"[send_notification] New Notification created (id={instance.id}) for user={instance.user_id}")

    # Send email notification via Celery
    try:
        if instance.user and instance.user.email:
            send_email_notification.delay(instance.id, instance.user.email)
            logger.info(f"[send_notification] Email notification task queued for user={instance.user.email}")
        else:
            logger.warning(f"[send_notification] Notification id={instance.id} has no associated user email. Email skipped.")
    except Exception as exc:
        logger.error(
            f"[send_notification] Failed to queue email notification for id={instance.id}: {exc}",
            exc_info=True
        )

    try:
        InAppNotification.objects.create(notification=instance)
        logger.info(f"[send_notification] In-app notification created for notification id={instance.id}")
    except Exception as exc:
        logger.error(
            f"[send_notification] Failed to create in-app notification for id={instance.id}: {exc}",
            exc_info=True
        )
