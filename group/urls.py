"""urls module"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_group),
    path('user/', views.add_users),
    path('delete/', views.delete_group),
    path('<int:group_id>/remove/<int:user_id>', views.remove_user),
]
