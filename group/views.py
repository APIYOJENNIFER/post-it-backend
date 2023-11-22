"""views module"""
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import Group
from .serializers import GroupSerializer


class PostItGroupApiView(APIView):
    """Define methods for performing actions on groups"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """Create a group"""
        data = request.data.copy()
        data['creator'] = request.user.id
        serializer = GroupSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        """Update members list"""
        data = request.data
        group_id = data.get("group_id")

        data.pop('creator', None)
        data.pop('name', None)
        try:
            group = Group.objects.get(id=group_id)
            if request.user != group.creator:
                return Response({
                                "error": "Only group creator can add members"},
                                status=status.HTTP_403_FORBIDDEN)
            errors = []
            for member in data.get("members"):
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

    def delete(self, request, group_id):
        """Delete a group"""
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


class PostItGroupDetailApiView(APIView):
    """
    Define methods for performing detail and more specific actions on groups
    """
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, user_id):
        """Delete/Remove a user from a specific group"""
        group_id = request.data.get("group_id")
        try:
            group = Group.objects.get(id=group_id)
            if request.user != group.creator:
                return Response({
                                "error":
                                "Only group creator can remove members"})
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
            return Response({"message":
                            f"User with ID {user_id} successfully removed"},
                            status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"error": f"User with ID {user_id} not found"},
                            status=status.HTTP_404_NOT_FOUND)
        except Group.DoesNotExist:
            return Response({"error": "Group not found"},
                            status=status.HTTP_404_NOT_FOUND)
