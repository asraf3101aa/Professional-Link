from django.urls import  path, include
from notification.views import InAppNotificationViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'notifications', InAppNotificationViewSet, basename='notification')

urlpatterns = [
    path('', include(router.urls)),
]