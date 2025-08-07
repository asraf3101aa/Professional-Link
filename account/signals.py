from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType


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
        thread_content_type = ContentType.objects.get_for_model(Thread)
        thread_permissions = Permission.objects.filter(
            content_type=thread_content_type,
            codename__in=[
                'add_thread',
                'change_thread', 
                'delete_thread',
                'view_thread'
            ]
        )
        
        # User permissions (excluding add_user for creation)
        user_content_type = ContentType.objects.get_for_model(User)
        user_permissions = Permission.objects.filter(
            content_type=user_content_type,
            codename__in=[
                'change_user',
                'delete_user',
                'view_user'
            ]
        )

        # Comment permissions
        comment_content_type = ContentType.objects.get_for_model(Comment)
        comment_permissions = Permission.objects.filter(
            content_type=comment_content_type,
            codename__in=[
                'add_comment',
                'change_comment',
                'delete_comment',
                'view_comment'
            ]
        )

        # Notification preference permissions
        notification_preference_ct = ContentType.objects.get_for_model(NotificationChannelPreference)
        notification_preference_permissions = Permission.objects.filter(
            content_type=notification_preference_ct,
            codename__in=[
                'change_notificationchannelpreference',
                'add_notificationchannelpreference',
                'view_notificationchannelpreference',
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
        all_permissions = list(thread_permissions) + list(user_permissions) + list(comment_permissions) + list(notification_preference_permissions) + list(in_app_notification_permissions)
        if all_permissions:
            instance.permissions.set(all_permissions)