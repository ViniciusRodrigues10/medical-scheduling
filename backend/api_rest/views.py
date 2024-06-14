from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from knox.models import AuthToken
from .models import CustomUser
from .serializers import CustomUserSerializer, EmailAuthTokenSerializer, UpdateUserSerializer, DoctorSerializer

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

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_data(request):
    try:
        user = request.user
    except CustomUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        serializer = UpdateUserSerializer(user, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user_account(request):
    try:
        user = request.user
    except CustomUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def register_doctor(request):
    data = request.data.copy()
    data['user']['user_type'] = 2

    serializer = DoctorSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    
    doctor = serializer.save()
    _, token = AuthToken.objects.create(doctor.user)

    return Response({
        'user_info': {
            'id_user': doctor.user.id_user,
            'email': doctor.user.email,
            'first_name': doctor.user.first_name,
            'last_name': doctor.user.last_name,
            'gender': doctor.user.gender,
            'telephone': doctor.user.telephone,
            'date_of_birth': doctor.user.date_of_birth,
            'user_type': doctor.user.user_type
        },
        'doctor_info': {
            'specialty': doctor.specialty,
            'crm': doctor.crm,
            'biography': doctor.biography
        },
        'token': token
    }, status=status.HTTP_201_CREATED)
