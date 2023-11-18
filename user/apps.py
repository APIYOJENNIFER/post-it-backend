"""App module"""
from django.apps import AppConfig


class UserConfig(AppConfig):
    """app class configuration"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'
