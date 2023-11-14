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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_users(request, group_id):
    """Add user(s) to a group"""
    if request.method == 'POST':
        members = request.data.get('members')
        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return Response({"error": "Group not found"},
                            status=status.HTTP_404_NOT_FOUND)
        for member in group.members.all():
            if member.id not in members:
                members.append(member.id)
        for member in members:
            user = User.objects.get(id=member)
            if user.id not in group.members.all().values_list('id', flat=True):
                group.members.add(user)
        serializer = GroupSerializer(group, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return None
