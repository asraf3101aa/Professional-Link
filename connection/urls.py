from django.urls import path
from connection.views import ConnectionRequestAPIView

urlpatterns = [
    path('request/', ConnectionRequestAPIView.as_view(), name='connection-request-create'),
    path('request/<int:pk>/', ConnectionRequestAPIView.as_view(), name='connection-request-update'),
]