"""urls module"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_group),
    path('user/', views.add_users),
    path('delete/', views.delete_group),
    path('remove/', views.remove_user),
]
