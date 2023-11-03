"""urls module"""
from django.urls import path
from .views import GroupApiView, GroupDetailApiView, MessageAPIView

urlpatterns = [
    path('', GroupApiView.as_view()),
    path('<int:group_id>/', GroupApiView.as_view()),
    path('detail/<int:group_id>/', GroupDetailApiView.as_view()),
    path('user/<int:user_id>/', GroupDetailApiView.as_view()),
    path('message', MessageAPIView.as_view()),
    path('<int:group_id>/user/', views.add_users),
    path('<int:group_id>/message/', views.post_message),
    path('<int:group_id>/messages/', views.retrieve_messages),
]