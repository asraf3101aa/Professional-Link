from django.contrib import admin
from .models import ConnectionRequest, Connection


@admin.register(ConnectionRequest)
class ConnectionRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "receiver", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = (
        "sender__username", "sender__email",
        "receiver__username", "receiver__email"
    )
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)

    def get_queryset(self, request):
        # Prefetch users for performance
        return super().get_queryset(request).select_related("sender", "receiver")


@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    list_display = ("id", "participant_one", "participant_two", "created_at")
    search_fields = (
        "participant_one__username", "participant_one__email",
        "participant_two__username", "participant_two__email"
    )
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)

    def get_queryset(self, request):
        # Prefetch users for performance
        return super().get_queryset(request).select_related("participant_one", "participant_two")
