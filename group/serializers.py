"""Serializer module"""
from rest_framework import serializers
from django.contrib.auth.models import User
from user.serializers import UserSerializer
from .models import Group


class GroupSerializer(serializers.ModelSerializer):
    """Group serializer class"""

    class Meta:
        """Serializer Meta class"""
        model = Group
        fields = ['id', 'name', 'members', 'creator']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['members'] = UserSerializer(
                                    instance.members, many=True).data
        return representation

    def update(self, instance, validated_data):
        new_members = validated_data.get("members")

        member_objects = User.objects.filter(
            id__in=[member.id for member in new_members])
        instance.members.add(*member_objects)
        instance.save()
        return instance
