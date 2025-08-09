from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from connection.models import ConnectionRequest
from notification.models import InAppNotification


User = get_user_model()

@receiver(post_save, sender=User)
def add_user_to_content_creator_group(sender, instance, created, **kwargs):
    if created:
        group, _ = Group.objects.get_or_create(name='end user')
        instance.groups.add(group)


@receiver(post_save, sender=Group)
def setup_content_creator_group_permissions(sender, instance, created, **kwargs):
    if created and instance.name == 'end user':
        # Thread permissions
        connection_request_content_type = ContentType.objects.get_for_model(ConnectionRequest)
        connection_request_permissions = Permission.objects.filter(
            content_type=connection_request_content_type,
            codename__in=[
                'add_connectionrequest',
                'change_connectionrequest', 
                'delete_connectionrequest',
                'view_connectionrequest'
            ]
        )
        
        user_content_type = ContentType.objects.get_for_model(User)
        user_permissions = Permission.objects.filter(
            content_type=user_content_type,
            codename__in=[
                'change_user',
                'delete_user',
                'view_user'
            ]
        )

        # In App Notification
        in_app_notification_content_type = ContentType.objects.get_for_model(InAppNotification)
        in_app_notification_permissions = Permission.objects.filter(
            content_type=in_app_notification_content_type,
            codename__in=[
                'change_inappnotification',
            ]
        )

        # Combine all permissions
        all_permissions = list(user_permissions) + list(connection_request_permissions) + list(in_app_notification_permissions)
        if all_permissions:
            instance.permissions.set(all_permissions)