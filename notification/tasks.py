import logging
from celery import shared_task
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail
from celery.exceptions import Retry
from notification.choices import EmailNotificationStatus
from notification.models import EmailNotification, Notification

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3, default_retry_delay=10) 
def send_email_notification(self, notification_id, receiver_email):
    try:
        notification = Notification.objects.get(id=notification_id)
    except Notification.DoesNotExist:
        logger.warning(f"[send_email_notification] Notification with id={notification_id} not found. Task aborted.")
        return

    title = notification.title
    content = notification.body
    from_email = settings.DEFAULT_EMAIL_SENDER
    recipient_list = [receiver_email]

    logger.info(f"[send_email_notification] Sending email to {receiver_email} for notification id={notification_id}.")

    # Create EmailNotification record
    email_notification = EmailNotification.objects.create(
        notification=notification
    )

    try:
        send_mail(
            title,
            content,
            from_email,
            recipient_list,
            fail_silently=False,
        )
    except Exception as exc:
        logger.error(f"[send_email_notification] Failed to send email to {receiver_email} for notification id={notification_id}: {exc}", exc_info=True)
        email_notification.status = EmailNotificationStatus.FAILED
        email_notification.error_message = str(exc)
        email_notification.save()

        try:
            logger.info(f"[send_email_notification] Retrying task for notification id={notification_id}, receiver={receiver_email}. Attempt {self.request.retries + 1}")
            raise self.retry(exc=exc)
        except Retry:
            logger.warning(f"[send_email_notification] Max retries reached for notification id={notification_id}, receiver={receiver_email}. Task failed permanently.")
            pass
    else:
        email_notification.status = EmailNotificationStatus.SENT
        email_notification.delivered_at = timezone.now()
        email_notification.error_message = None
        email_notification.save()
        logger.info(f"[send_email_notification] Email successfully sent to {receiver_email} for notification id={notification_id}.")
