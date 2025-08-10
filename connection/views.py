import logging
from rest_framework import status
from connection.choices import RequestStatus
from connection.models import Connection, ConnectionRequest
from connection.serializers import ConnectionRequestSerializer, RequestStatusSerializer
from core.utils.custom_response import CustomResponse
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from django.db import transaction
from notification.models import Notification

User = get_user_model()
logger = logging.getLogger(__name__)


class ConnectionRequestAPIView(APIView):
    def post(self, request):
        logger.info("Connection request POST attempt by user: %s with data: %s", request.user, request.data)
        
        try:
            serializer = ConnectionRequestSerializer(data=request.data, context={'request': request})
            if not serializer.is_valid():
                logger.warning("Connection request serializer invalid: %s", serializer.errors)
                return CustomResponse(
                    data=serializer.errors,
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            serializer.save(sender=request.user)
            logger.info("Connection request created successfully: %s", serializer.data)

            return CustomResponse(serializer.data, status_code=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error("Exception during connection request creation: %s", str(e), exc_info=True)

            return CustomResponse(
                data=e,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def patch(self, request, pk=None):
        logger.info("PATCH connection request %s by user %s with data: %s", pk, request.user, request.data)

        try:
            with transaction.atomic():
                user = request.user
                connection_request = ConnectionRequest.objects.filter(
                    pk=pk, status=RequestStatus.PENDING, receiver=user
                ).first()
                if not connection_request:
                    logger.warning("Connection request %s not found or not pending for user %s", pk, user)
                    return CustomResponse(
                        data="Connection request not found.",
                        status_code=status.HTTP_404_NOT_FOUND
                    )
                
                serializer = RequestStatusSerializer(data=request.data)
                if not serializer.is_valid():
                    logger.warning("RequestStatusSerializer invalid for connection request %s: %s", pk, serializer.errors)
                    return CustomResponse(
                        data=serializer.errors,
                        status_code=status.HTTP_400_BAD_REQUEST
                    )
                
                new_status = serializer.validated_data['status']
                connection_request.status = new_status
                connection_request.save()
                logger.info("Connection request %s status updated to %s", pk, new_status)

                if new_status == RequestStatus.ACCEPTED:
                    sender = connection_request.sender
                    receiver = connection_request.receiver

                    exists = Connection.objects.filter(
                        participant_one__in=[sender, receiver],
                        participant_two__in=[sender, receiver]
                    ).exists()

                    if not exists:
                        Connection.objects.create(
                            participant_one=sender,
                            participant_two=receiver
                        )
                        logger.info("New Connection created between %s and %s", sender, receiver)

                Notification.objects.create(
                    user = sender,
                    title = f"Connection Request {new_status}",
                    body = f"{receiver.username} has {new_status} your connection request.",
                )
                
                response_data = ConnectionRequestSerializer(connection_request).data
                return CustomResponse(data=response_data)
        
        except Exception as e:
            logger.error("Exception during PATCH connection request %s: %s", pk, str(e), exc_info=True)
            return CustomResponse(
                data=e,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )