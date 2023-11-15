"""urls module"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_group),
    path('<int:group_id>/user/', views.add_users),
    path('<int:group_id>/delete/', views.delete_group),
    path('<int:group_id>/remove/<int:user_id>', views.remove_user),
]
