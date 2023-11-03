from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import Group, Message
from .serializers import GroupSerializer, MessageSerializer

# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_group(request):
    if request.method == 'POST':
        data = request.data.copy()
        data['creator']=request.user.id
        serializer = GroupSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_users(request, group_id):
    """Add user(s) to a group"""
    if request.method == 'POST':
        members = request.data.get('members')
        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return Response({"error":"Group not found"}, status=status.HTTP_404_NOT_FOUND)
        
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
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_message(request, group_id):
    """Post message to a group"""
    if request.method == 'POST':
        try:
            group = Group.objects.get(id=group_id)
            user = request.user
        except Group.DoesNotExist:
            return Response({"error":"Group not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if user in group.members.all():
            data = {
                "post": request.data.get("post"),
                "group": group.id,
                "user":user.id,
            }
        
            serializer = MessageSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error":"User is not a member of this group"}, status=status.HTTP_403_FORBIDDEN)
        

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def retrieve_messages(request, group_id):
    if request.method == 'GET':
        try:
            group = Group.objects.get(id=group_id)
            user = request.user
        except Group.DoesNotExist:
            return Response({"error":"Group not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if user in group.members.all():
            messages = Message.objects.filter(group=group)

            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error":"User is not a member of this group"}, status=status.HTTP_403_FORBIDDEN)
