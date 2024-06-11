from rest_framework.decorators import api_view
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import CustomUserSerializer
from rest_framework import status

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
