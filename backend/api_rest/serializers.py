from rest_framework import serializers
from .models import (
    CustomUser,
    Doctor,
    Availability,
    Appointment,
    EmergencyContact,
    MedicalHistory,
    LifeHabits,
    AdditionalInformation,
)
from .facade.serializer_facade import (
    UserCreatorFacade,
    ValidateEmailForRegistrationFacade,
    ValidateLoginFacade,
)


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id_user",
            "email",
            "password",
            "first_name",
            "last_name",
            "gender",
            "user_type",
            "is_staff",
            "is_superuser",
        ]
        extra_kwargs = {
            "email": {"required": True},
            "password": {"write_only": True, "required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
            "gender": {"required": True},
        }

    def create(self, validated_data):
        create_user = UserCreatorFacade(self.Meta.model)

        return create_user.create_user(validated_data)


class AdditionalInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalInformation
        fields = [
            "user",
            "telephone",
            "date_of_birth",
            "completed_form",
        ]


class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = ["id", "name", "phone_number"]


class MedicalHistorySerializer(serializers.ModelSerializer):
    emergency_contacts = EmergencyContactSerializer(many=True)

    class Meta:
        model = MedicalHistory
        fields = [
            "id_medical_history",
            "id_user",
            "current_medications",
            "allergies",
            "surgeries",
            "family_history",
            "blood_type",
            "emergency_contacts",
        ]

    def create(self, validated_data):
        emergency_contacts_data = validated_data.pop("emergency_contacts")
        medical_history = MedicalHistory.objects.create(**validated_data)

        for contact_data in emergency_contacts_data:
            emergency_contact = EmergencyContact.objects.create(**contact_data)
            medical_history.emergency_contacts.add(emergency_contact)

        return medical_history

    def update(self, instance, validated_data):
        emergency_contacts_data = validated_data.pop("emergency_contacts")
        instance.current_medications = validated_data.get(
            "current_medications", instance.current_medications
        )
        instance.allergies = validated_data.get("allergies", instance.allergies)
        instance.surgeries = validated_data.get("surgeries", instance.surgeries)
        instance.family_history = validated_data.get(
            "family_history", instance.family_history
        )
        instance.blood_type = validated_data.get("blood_type", instance.blood_type)
        instance.health_plan = validated_data.get("health_plan", instance.health_plan)
        instance.save()

        instance.emergency_contacts.clear()

        for contact_data in emergency_contacts_data:
            emergency_contact, created = EmergencyContact.objects.get_or_create(
                **contact_data
            )
            instance.emergency_contacts.add(emergency_contact)

        return instance


class LifeHabitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LifeHabits
        fields = "__all__"


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email", "first_name", "last_name", "gender"]
        extra_kwargs = {"email": {"required": True}}

    def validate_email(self, email):
        user = self.context["request"].user
        email_validator = ValidateEmailForRegistrationFacade(user, CustomUser)

        return email_validator.evaluates_whether_email_is_in_use(email)


class EmailAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        validate_login = ValidateLoginFacade(attrs, self.context)
        return validate_login.validate()


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ["user", "specialty", "crm", "biography"]


class AvailabilitySerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(
        source="id_doctor.user.get_full_name", read_only=True
    )
    specialty = serializers.CharField(source="id_doctor.specialty", read_only=True)

    class Meta:
        model = Availability
        fields = [
            "id_doctor",
            "date",
            "start_time",
            "end_time",
            "doctor_name",
            "specialty",
        ]


class UpdateAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ["date", "start_time", "end_time"]


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = [
            "id_appointment",
            "id_user",
            "id_professional",
            "date",
            "start_time",
            "end_time",
            "created_at",
        ]
