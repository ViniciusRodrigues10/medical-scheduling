from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from knox.models import AuthToken
from .serializers import CustomUserSerializer, EmailAuthTokenSerializer

@api_view(['POST'])
def register_patient_api(request):
    data = request.data.copy()
    data['user_type'] = 1

    serializer = CustomUserSerializer(data=data)
    serializer.is_valid(raise_exception=True)

    user = serializer.save()
    _, token = AuthToken.objects.create(user)

    return Response({
        'user_info': {
            'id_user': user.id_user,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'gender': user.gender,
            'telephone': user.telephone,
            'date_of_birth': user.date_of_birth,
            'user_type': user.user_type
        },
        'token': token
    }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login_api(request):
    serializer = EmailAuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']

    _, token = AuthToken.objects.create(user)

    return Response({
        'user_info': {
            'id_user': user.id_user,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'gender': user.gender,
            'telephone': user.telephone,
            'date_of_birth': user.date_of_birth,
            'user_type': user.user_type
        },
        'token': token
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_data(request):
    user = request.user

    return Response({
        'user_info': {
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'gender': user.gender,
            'telephone': user.telephone,
            'date_of_birth': user.date_of_birth,
        },
    }, status=status.HTTP_200_OK)
