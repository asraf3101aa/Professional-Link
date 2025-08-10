from django.contrib import admin
from .models import Notification, InAppNotification, EmailNotification


class InAppNotificationInline(admin.TabularInline):
    model = InAppNotification
    extra = 0
    readonly_fields = ("created_at", "read_at", "status")
    can_delete = False


class EmailNotificationInline(admin.TabularInline):
    model = EmailNotification
    extra = 0
    readonly_fields = ("created_at", "delivered_at", "error_message", "status")
    can_delete = False


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "notification_type", "get_in_app_count", "get_email_count")
    search_fields = ("title", "body", "user__username", "user__email")
    list_filter = ("notification_type",)
    inlines = [InAppNotificationInline, EmailNotificationInline]

    def get_in_app_count(self, obj):
        return obj.in_app_notifications.count()
    get_in_app_count.short_description = "In-App Count"

    def get_email_count(self, obj):
        return obj.email_notifications.count()
    get_email_count.short_description = "Email Count"


@admin.register(InAppNotification)
class InAppNotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "notification", "status", "created_at", "read_at")
    list_filter = ("status",)
    search_fields = ("notification__title", "notification__user__username", "notification__user__email")
    readonly_fields = ("created_at",)


@admin.register(EmailNotification)
class EmailNotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "notification", "status", "created_at", "delivered_at", "error_message")
    list_filter = ("status",)
    search_fields = ("notification__title", "notification__user__username", "notification__user__email")
    readonly_fields = ("created_at",)
