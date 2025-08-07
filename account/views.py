from account.serializers import LoginSerializer, UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework import viewsets, status
from rest_framework.views import APIView
from core.custom_response import CustomResponse
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import update_last_login

User = get_user_model()


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if not serializer.is_valid:
                return CustomResponse(
                    data=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user = serializer.validated_data.get('user')
            auth_tokens = RefreshToken.for_user(user)
            update_last_login(None, user)
            data = {
                'access_token': str(auth_tokens.access_token),
                'refresh_token': str(auth_tokens)
            }
            return CustomResponse(data=data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return CustomResponse(
                data=e,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserViewSet(viewsets.ViewSet):
    def create(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if not serializer.is_valid():
                return CustomResponse(
                    data=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer.save()
            return CustomResponse(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return CustomResponse(
                data=e,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )