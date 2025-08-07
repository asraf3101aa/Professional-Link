from django.urls import  path, include
from account.views import   LoginView, UserViewSet
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='user_login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]