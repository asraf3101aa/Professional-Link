import logging
from account.serializers import LoginSerializer, UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, DjangoModelPermissions, IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.views import APIView
from core.utils.custom_response import CustomResponse
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import update_last_login
from core.utils.pagination import CustomPagination
from django.db.models import Q

User = get_user_model()
logger = logging.getLogger(__name__)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        logger.info("Login attempt for username: %s", request.data.get('username', 'unknown'))

        try:
            serializer = LoginSerializer(data=request.data)
            if not serializer.is_valid():
                logger.warning("Login serializer invalid: %s", serializer.errors)

                return CustomResponse(
                    data=serializer.errors,
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            
            user = serializer.validated_data.get('user')
            logger.info("User %s authenticated successfully", user.email)
            auth_tokens = RefreshToken.for_user(user)
            update_last_login(None, user)
            data = {
                'access_token': str(auth_tokens.access_token),
                'refresh_token': str(auth_tokens)
            }
            logger.debug("Tokens generated for user %s", user.email)
            return CustomResponse(data=data, status_code=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error("Exception during login: %s", str(e), exc_info=True)
            return CustomResponse(
                data=e,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserViewSet(viewsets.ViewSet):
    pagination_class = CustomPagination
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        elif self.action == 'list':
            return [DjangoModelPermissions()]
        else:
            return [IsAuthenticated()]
        
    def get_queryset(self):
        return User.objects.all()


    def create(self, request):
        logger.info("User creation attempt with data: %s", request.data)

        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                logger.warning("User creation serializer invalid: %s", serializer.errors)
                return CustomResponse(
                    data=serializer.errors,
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            serializer.save()
            logger.info("User created successfully: %s", serializer.data)
            return CustomResponse(
                data=serializer.data,
                status_code=status.HTTP_201_CREATED
            )

        except Exception as e:
            logger.error("Exception during user creation: %s", str(e), exc_info=True)
            return CustomResponse(
                data=e,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    """
    Search users by name, company name, email, or contact number.
    """
    def list(self, request):
        try:
            search_query = request.query_params.get('search', '').strip()

            if len(search_query) > 100:
                return CustomResponse(
                    data={"search": ["Search query too long"]},
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            
            queryset = self.get_queryset()

            if search_query:
                queryset = queryset.filter(
                    Q(full_name__icontains=search_query) |
                    Q(company_name__icontains=search_query) |
                    Q(email__icontains=search_query) |
                    Q(contact_number__icontains=search_query)
                )

            paginator = self.pagination_class()
            page = paginator.paginate_queryset(queryset, request)
            serializer = self.serializer_class(page, many=True)
            users = {"users": serializer.data}
            response_data = paginator.get_paginated_response(users)
            return CustomResponse(
                data=response_data,
            )        
        except Exception as e:
            return CustomResponse(
                data=e,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )