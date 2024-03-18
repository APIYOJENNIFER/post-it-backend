"""views module"""
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination

from django.contrib.auth.models import User
from django.http import Http404


from .models import Group, Message
from .serializers import GroupSerializer, MessageSerializer


class GroupApiView(ListAPIView):
    """Define methods for performing actions on groups"""
    permission_classes = [permissions.IsAuthenticated]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = PageNumberPagination

    def get_object(self, request=None, group_id=None):
        """Check for user permission and group existence"""
        try:
            if request and group_id is not None:
                group = Group.objects.get(id=group_id)
                if request.user != group.creator:
                    raise PermissionDenied("Access Denied")
            return group
        except Group.DoesNotExist as exc:
            raise Http404 from exc

    def get(self, request, *args, **kwargs):
        """Retrieve a list of all the groups"""
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Create a group"""
        data = request.data.copy()
        user_id = request.user.id
        data['creator'] = user_id
        data['members'] = [user_id]
        serializer = GroupSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        """Update members list"""
        data = request.data
        group_id = data.get("group_id")
        members_ids = data.get("members")

        data.pop('creator', None)
        data.pop('name', None)
        try:
            group = self.get_object(request, group_id)
            errors = []
            for member in members_ids:
                try:
                    user = User.objects.get(id=member)
                    group.members.add(user)
                except User.DoesNotExist:
                    errors.append(f"User with ID {member} is not found")
            serializer = GroupSerializer(group, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            if errors:
                return Response({"error": errors},
                                status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied:
            return Response({"error": "Only group creator can add members"},
                            status=status.HTTP_403_FORBIDDEN)
        except Http404:
            return Response({"error": "Group not found"},
                            status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, group_id):
        """Delete a group"""
        try:
            group = self.get_object(request, group_id)
            group.delete()
            return Response({"message": "Group deleted successfully"},
                            status=status.HTTP_204_NO_CONTENT)
        except PermissionDenied:
            return Response({"error": "Only the group creator can delete"},
                            status=status.HTTP_403_FORBIDDEN)
        except Http404:
            return Response({"error": "Group not found"},
                            status=status.HTTP_404_NOT_FOUND)


class GroupDetailApiView(APIView):
    """
    Define methods for performing detail and more specific actions on groups
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, group_id):
        """Retrieve a single group"""
        try:
            group = Group.objects.get(id=group_id)
            serializer = GroupSerializer(group)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Group.DoesNotExist:
            return Response({"error": "Group not found"},
                            status=status.HTTP_404_NOT_FOUND)

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
            if user.id == group.creator.id:
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


class MessageAPIView(APIView):
    """Define methods for messaging within the group"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """Post message to a group"""
        data = request.data
        group_id = data.get("group_id")
        post = data.get("post")
        try:
            group = Group.objects.select_related("creator").get(id=group_id)
            user = request.user
        except Group.DoesNotExist:
            return Response({"error": "Group not found"},
                            status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({"error": "User not found"},
                            status=status.HTTP_404_NOT_FOUND)
        if user.id in group.members.all().values_list("id", flat=True):
            data = {
                "post": post,
                "group": group.id,
                "user": user.id,
            }

            serializer = MessageSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "User is not a member of this group"},
                        status=status.HTTP_403_FORBIDDEN)


class MessageDetailAPIView(APIView):
    """Define methods for messaging within the group"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """Retrieve all messages in a group"""
        group_id = kwargs.get("group_id")
        user_id = kwargs.get("user_id")
        try:
            group = Group.objects.select_related("creator").get(id=group_id)
            user = User.objects.select_related("auth_token").get(id=user_id)
        except Group.DoesNotExist:
            return Response({"error": "Group not found"},
                            status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({"error": "User not found"},
                            status=status.HTTP_404_NOT_FOUND)

        if user.id in group.members.all().values_list("id", flat=True):
            messages = Message.objects.filter(group=group)

            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "User is not a member of this group"},
                        status=status.HTTP_403_FORBIDDEN)
