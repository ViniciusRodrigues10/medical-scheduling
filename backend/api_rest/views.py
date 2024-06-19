from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import CustomUser, Doctor, Availability
from knox.models import AuthToken
from django.db.models import Q
from .serializers import CustomUserSerializer, EmailAuthTokenSerializer, UpdateUserSerializer, DoctorSerializer, AvailabilitySerializer, UpdateAvailabilitySerializer

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

# TODO: Add restriction, only superuser and administrator can register doctors
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_doctor_data(request):
    try:
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)

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
    }, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_doctor_data(request):
    try:
        doctor = Doctor.objects.get(user=request.user)
    except CustomUser.DoesNotExist:
        return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = DoctorSerializer(doctor, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# TODO: add restriction, only superuser and admin can delete doctors
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_doctor_account(request):
    try:
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    user = doctor.user
    doctor.delete()
    user.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)


# TODO: possibly remove the GET
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def availability_list_create(request):
    if request.method == 'GET':
        user = request.user
        availabilities = Availability.objects.filter(id_professional__user=user)
        serializer = AvailabilitySerializer(availabilities, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST': 
        data = request.data.copy()
        data['id_professional'] = Doctor.objects.get(user=request.user).pk
        serializer = AvailabilitySerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def availability_list(request):
    query_params = request.query_params
    doctor_name = query_params.get('doctor_name', None)
    specialty = query_params.get('specialty', None)

    availabilities = Availability.objects.all()

    if doctor_name: 
        availabilities = availabilities.filter(
            Q(id_professional__user__first_name__icontains=doctor_name) |
            Q(id_professional__user__last_name__icontains=doctor_name)
        )
    
    if specialty:
        availabilities = availabilities.filter(
            Q(id_professional__specialty__icontains=specialty)
        )

    serializer = AvailabilitySerializer(availabilities, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_availability(request):
    try:
        user = request.user
        doctor = Doctor.objects.get(user=user)
        date = request.data.get('date')
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')
        
        availability = Availability.objects.get(id_professional=doctor, date=date, start_time=start_time, end_time=end_time)
    except Availability.DoesNotExist:
        return Response({"error": "Availability not found"}, status=status.HTTP_404_NOT_FOUND)
    
    update_data = {
        'date': request.data.get('new_date', availability.date),
        'start_time': request.data.get('new_start_time', availability.start_time),
        'end_time': request.data.get('new_end_time', availability.end_time)
    }
    
    serializer = UpdateAvailabilitySerializer(availability, data=update_data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
