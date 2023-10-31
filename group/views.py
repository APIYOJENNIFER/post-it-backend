"""views module"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
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
