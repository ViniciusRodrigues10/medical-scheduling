from rest_framework import serializers
from .models import CustomUser, Doctor, Availability, Appointment
from .facade.serializer_facade import UserCreatorFacade, ValidateEmailForRegistrationFacade, ValidateLogin, DoctorFacade

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
        create_user = UserCreatorFacade(self.Meta.model)

        return create_user.create_user(validated_data)
    
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'gender', 'telephone', 'date_of_birth']
        extra_kwargs = {
            'email': {'required': True}
        }

    def validate_email(self, email):
        user = self.context['request'].user
        email_validator = ValidateEmailForRegistrationFacade(user, CustomUser)

        return email_validator.evaluates_whether_email_is_in_use(email)

class EmailAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        validate_login = ValidateLogin(attrs, self.context)
        return validate_login.validate()
    
class DoctorSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Doctor
        fields = ['user', 'specialty', 'crm', 'biography']
    
    def create(self, validated_data):
        doctor = DoctorFacade()
        return doctor.create_doctor(validated_data)

    def update(self, instance, validated_data):
        doctor = DoctorFacade()
        return doctor.update_doctor(instance, validated_data)

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

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id_appointment', 'id_user', 'id_professional', 'date', 'start_time', 'end_time', 'created_at']
