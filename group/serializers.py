"""Serializer module"""
from rest_framework import serializers
from .models import Group


class GroupSerializer(serializers.ModelSerializer):
    """Group seerializer class"""
    class Meta:
        """Serializer Meta class"""
        model = Group
        fields = ['id', 'name', 'members', 'creator']
