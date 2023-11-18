"""Apps module"""
from django.apps import AppConfig


class GroupConfig(AppConfig):
    """App class configuration"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'group'
