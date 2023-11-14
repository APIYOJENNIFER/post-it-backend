"""urls module"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_group),
    path('<int:group_id>/user/', views.add_users),
    path('<int:group_id>/delete/', views.delete_group),
]
