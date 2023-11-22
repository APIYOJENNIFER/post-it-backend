"""Serializer module"""
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Group


class GroupSerializer(serializers.ModelSerializer):
    """Group seerializer class"""
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
