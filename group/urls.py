"""urls module"""
from django.urls import path
from .views import GroupApiView, GroupDetailApiView

urlpatterns = [
    path('', GroupApiView.as_view()),
    path('<int:group_id>/', GroupApiView.as_view()),
    path('detail/<int:group_id>/', GroupDetailApiView.as_view()),
    path('user/<int:user_id>/', GroupDetailApiView.as_view()),
    path('message', GroupDetailApiView.as_view()),
]
