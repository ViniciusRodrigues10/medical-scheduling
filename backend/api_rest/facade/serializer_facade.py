# TODO: Remove facade rules, make an archive with the rules
from rest_framework import serializers
from django.contrib.auth import authenticate
from ..models import CustomUser, Doctor
from ..factories.serializer_factories import (
    SerializerUserFactory,
    ValidateEmailForRegistrationFactory,
    ValidadeLoginFactory,
    SerializerDoctorFactory,
)
from ..singleton.singleton import RequestLogger
from ..decorator.decorators import log_request

logger = RequestLogger()


class UserCreatorFacade(SerializerUserFactory):
    def __init__(self, model) -> None:
        self.model = model

    def create_user(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.model(**validated_data)

        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance


class ValidateEmailForRegistrationFacade(ValidateEmailForRegistrationFactory):
    def __init__(self, user, class_user) -> None:
        self.user = user
        self.class_user = class_user

    def evaluates_whether_email_is_in_use(self, email):
        if (
            self.class_user.objects.exclude(pk=self.user.id_user)
            .filter(email=email)
            .exists()
        ):
            raise serializers.ValidationError("This email is already in use")

        return email


@log_request(logger)
class ValidateLoginFacade(ValidadeLoginFactory):
    def __init__(self, attrs, context):
        self.attrs = attrs
        self.context = context
        self.email = self.attrs.get("email")
        self.password = self.attrs.get("password")
        self.user = None

    @log_request(logger)
    def validate(self):
        if self.email and self.password:
            self.user = authenticate(
                request=self.context.get("request"),
                email=self.email,
                password=self.password,
            )

            if not self.user:
                raise serializers.ValidationError(
                    "Invalid email or password.", code="authorization"
                )
        else:
            raise serializers.ValidationError(
                'Must include "email" and "password".', code="authorization"
            )

        self.attrs["user"] = self.user

        return self.attrs


class DoctorFacade(SerializerDoctorFactory):
    def create_doctor(self, validated_data):
        user_data = validated_data.pop("user")
        self.user = CustomUser.objects.create_user(**user_data)
        doctor = Doctor.objects.create(user=self.user, **validated_data)

        return doctor

    def update_doctor(self, instance, validated_data):
        user_data = validated_data.pop("user")
        user = instance.user

        instance.specialty = validated_data.get("specialty", instance.specialty)
        instance.crm = validated_data.get("crm", instance.crm)
        instance.biography = validated_data.get("biography", instance.biography)
        instance.save()

        user.first_name = user_data.get("first_name", user.first_name)
        user.last_name = user_data.get("last_name", user.last_name)
        user.email = user_data.get("email", user.email)
        user.gender = user_data.get("gender", user.gender)
        user.telephone = user_data.get("telephone", user.telephone)
        user.date_of_birth = user_data.get("date_of_birth", user.date_of_birth)
        user.save()

        return instance
