"""Serializer module"""
from rest_framework import serializers
from django.contrib.auth.models import User
from user.serializers import UserSerializer
from .models import Group


class GroupGetSerializer(serializers.ModelSerializer):
    """Group GET method serializer class"""
    members = UserSerializer(many=True)

    class Meta:
        """Serializer Meta class"""
        model = Group
        fields = ['id', 'name', 'members', 'creator']


class GroupSerializer(serializers.ModelSerializer):
    """Group serializer class"""
    class Meta:
        """Serializer Meta class"""
        model = Group
        fields = ['id', 'name', 'members', 'creator']

    def update(self, instance, validated_data):
        existing_members = instance.members.all()
        new_members = validated_data.get("members")

        for member in new_members:
            if member not in existing_members:
                user = User.objects.get(id=member)
                instance.members.add(user)
        instance.save()
        return instance
