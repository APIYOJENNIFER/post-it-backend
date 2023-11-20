"""views module"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import Group
from .serializers import GroupSerializer

# Create your views here.


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_group(request):
    """function based view for creating a group"""
    if request.method == 'POST':
        data = request.data.copy()
        data['creator'] = request.user.id
        serializer = GroupSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return None


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def add_users(request):
    """Add user(s) to a group"""
    if request.method == 'PATCH':
        data = request.data.copy()
        group_id = request.data.get("group_id")

        data.pop('creator', None)
        data.pop('name', None)
        try:
            group = Group.objects.get(id=group_id)
            if request.user != group.creator:
                return Response({
                                "error": "Only group creator can add members"},
                                status=status.HTTP_403_FORBIDDEN)
            errors = []
            for member in group.members.all():
                if member.id not in data['members']:
                    data['members'].append(member.id)
            for member in data['members']:
                try:
                    user = User.objects.get(id=member)
                    if user.id not in group.members.all()\
                            .values_list('id', flat=True):
                        group.members.add(user)
                except User.DoesNotExist:
                    errors.append(f"User with ID {member} is not found")
            serializer = GroupSerializer(group, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            if errors:
                return Response({"error": errors},
                                status=status.HTTP_404_NOT_FOUND)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        except Group.DoesNotExist:
            return Response({"error": "Group not found"},
                            status=status.HTTP_404_NOT_FOUND)
    return None


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_group(request):
    """Delete a group"""
    if request.method == 'DELETE':
        group_id = request.data.get("group_id")
        try:
            group = Group.objects.get(id=group_id)
            if request.user != group.creator:
                return Response({"error": "Only the group creator can delete"})
            group.delete()
            return Response({"message": "Group deleted successfully"},
                            status=status.HTTP_204_NO_CONTENT)
        except Group.DoesNotExist:
            return Response({"error": "Group not found"},
                            status=status.HTTP_404_NOT_FOUND)
    return None


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_user(request):
    """Remove a user(s) from a group"""
    if request.method == 'DELETE':
        group_id = request.data.get("group_id")
        user_id = request.data.get("user_id")
        try:
            group = Group.objects.get(id=group_id)
            if request.user != group.creator:
                return Response({
                                "error":
                                "Only group creator can remove members"})
            try:
                user = User.objects.get(id=user_id)
                if user == group.creator:
                    return Response(
                        {"error": "Cannot remove creator from the group"},
                        status=status.HTTP_403_FORBIDDEN)
                if user.id not in group.members.all().values_list('id',
                                                                  flat=True):
                    return Response(
                        {"error": f"User with ID {user_id} not in this group"})
                group.members.remove(user)
            except User.DoesNotExist:
                return Response({"error": f"User with ID {user_id} not found"},
                                status=status.HTTP_404_NOT_FOUND)
            return Response({"message": "Member(s) successfully removed"},
                            status=status.HTTP_204_NO_CONTENT)
        except Group.DoesNotExist:
            return Response({"error": "Group not found"},
                            status=status.HTTP_404_NOT_FOUND)
    return None
