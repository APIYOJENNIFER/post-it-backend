"""urls module"""
from django.urls import path
from .views import PostItGroupApiView, PostItGroupDetailApiView

urlpatterns = [
    path('', PostItGroupApiView.as_view()),
    path('<int:group_id>/', PostItGroupApiView.as_view()),
    path('remove_user/<int:user_id>/', PostItGroupDetailApiView.as_view()),
]
