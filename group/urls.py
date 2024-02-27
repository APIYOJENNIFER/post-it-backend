"""urls module"""
from django.urls import path
from .views import GroupApiView, GroupDetailApiView, MessageAPIView

urlpatterns = [
    path('', GroupApiView.as_view()),
    path('<int:group_id>/', GroupApiView.as_view()),
    path('detail/<int:group_id>/', GroupDetailApiView.as_view()),
    path('users/<int:user_id>/', GroupDetailApiView.as_view()),
    path('messages', MessageAPIView.as_view()),
    path('messages/<int:user_id>/', MessageAPIView.as_view()),
]
