from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser, Doctor, Availability

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id_user', 'email', 'password', 'first_name', 'last_name', 'gender', 'telephone', 'date_of_birth', 'user_type']
        extra_kwargs = {
            'email': {'required': True},
            'password': {'write_only': True, 'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'gender': {'required': True},
            'telephone': {'required': True},
            'date_of_birth': {'required': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'gender', 'telephone', 'date_of_birth']
        extra_kwargs = {
            'email': {'required': True}
        }

    def validate_email(self, value):
        user = self.context['request'].user
        if CustomUser.objects.exclude(pk=user.id_user).filter(email=value).exists():
            raise serializers.ValidationError('This email is already in use')
        return value

class EmailAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)

            if not user:
                raise serializers.ValidationError('Invalid email or password.', code='authorization')
        else:
            raise serializers.ValidationError('Must include "email" and "password".', code='authorization')

        attrs['user'] = user
        return attrs
    
class DoctorSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Doctor
        fields = ['user', 'specialty', 'crm', 'biography']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = CustomUser.objects.create_user(**user_data)
        doctor = Doctor.objects.create(user=user, **validated_data)

        return doctor
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user

        instance.specialty = validated_data.get('specialty', instance.specialty)
        instance.crm = validated_data.get('crm', instance.crm)
        instance.biography = validated_data.get('biography', instance.biography)
        instance.save()

        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.email = user_data.get('email', user.email)
        user.gender = user_data.get('gender', user.gender)
        user.telephone = user_data.get('telephone', user.telephone)
        user.date_of_birth = user_data.get('date_of_birth', user.date_of_birth)
        user.save()

        return instance

class AvailabilitySerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='id_professional.user.get_full_name', read_only=True)
    specialty = serializers.CharField(source='id_professional.specialty', read_only=True)

    class Meta:
        model = Availability
        fields = ['id_availability', 'id_professional', 'date', 'start_time', 'end_time', 'doctor_name', 'specialty']

class UpdateAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ['date', 'start_time', 'end_time']
        