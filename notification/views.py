import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from core.utils.custom_response import CustomResponse
from core.utils.pagination import CustomPagination
from notification.models import InAppNotification
from notification.serializers import InAppNotificationSerializer

logger = logging.getLogger(__name__)


class InAppNotificationViewSet(viewsets.ViewSet):
    pagination_class = CustomPagination

    def list(self, request):
        try:
            queryset = InAppNotification.objects.filter(notification__user=request.user)
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(queryset, request)
            serializer = InAppNotificationSerializer(page, many=True)
            notifications = {"notifications": serializer.data}
            response_data = paginator.get_paginated_response(notifications)
            return CustomResponse(
                data=response_data,
            )          
        except Exception as e:
            logger.error(f"[InAppNotificationViewSet:list] Error: {e}", exc_info=True)

            return CustomResponse(
                data=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, pk=None):
        try:
            notification = InAppNotification.objects.filter(
                pk=pk, notification__user=request.user
            ).first()

            if not notification:
                return CustomResponse(
                    data="Notification not found.",
                    status_code=status.HTTP_404_NOT_FOUND
                )
            
            serializer = InAppNotificationSerializer(notification)
            return CustomResponse(data=serializer.data)
        except Exception as e:
            logger.error(f"[InAppNotificationViewSet:retrieve] Error: {e}", exc_info=True)
            return CustomResponse(
                data=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def create(self, request):
        try:
            serializer = InAppNotificationSerializer(data=request.data)
            if not serializer.is_valid():
                return CustomResponse(data=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)
            
            notification_obj = serializer.validated_data['notification']
            if notification_obj.user != request.user:
                return CustomResponse(
                    data="Cannot create notification for another user.",
                    status_code=status.HTTP_403_FORBIDDEN
                )
            
            serializer.save()
            return CustomResponse(data=serializer.data, status_code=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"[InAppNotificationViewSet:create] Error: {e}", exc_info=True)
            return CustomResponse(
                data=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def update(self, request, pk=None):
        try:
            notification = InAppNotification.objects.filter(
                pk=pk, notification__user=request.user
            ).first()

            if not notification:
                return CustomResponse(
                    data="Notification not found.",
                    status_code=status.HTTP_404_NOT_FOUND
                )

            serializer = InAppNotificationSerializer(notification, data=request.data)
            if not serializer.is_valid():
                return CustomResponse(data=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return CustomResponse(data=serializer.data)
        except Exception as e:
            logger.error(f"[InAppNotificationViewSet:update] Error: {e}", exc_info=True)
            return CustomResponse(
                data=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def partial_update(self, request, pk=None):
        try:
            notification = InAppNotification.objects.filter(
                pk=pk, notification__user=request.user
            ).first()

            if not notification:
                return CustomResponse(
                    data="Notification not found.",
                    status_code=status.HTTP_404_NOT_FOUND
                )

            serializer = InAppNotificationSerializer(notification, data=request.data, partial=True)
            if not serializer.is_valid():
                return CustomResponse(data=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return CustomResponse(data=serializer.data)
        except Exception as e:
            logger.error(f"[InAppNotificationViewSet:partial_update] Error: {e}", exc_info=True)
            return CustomResponse(
                data=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    def destroy(self, request, pk=None):
        try:
            notification = InAppNotification.objects.filter(
                pk=pk, notification__user=request.user
            ).first()

            if not notification:
                return CustomResponse(
                    data="Notification not found.",
                    status_code=status.HTTP_404_NOT_FOUND
                )

            notification.delete()
            return CustomResponse(data="Notification deleted successfully.", status_code=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(f"[InAppNotificationViewSet:destroy] Error: {e}", exc_info=True)
            return CustomResponse(
                data=str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
