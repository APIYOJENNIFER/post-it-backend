"""urls module"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_group),
    path('<int:group_id>/user/', views.add_users),
]
