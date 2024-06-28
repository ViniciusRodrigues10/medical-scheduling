# TODO: Remove facade rules, make an archive with the rules
from rest_framework import serializers
from django.contrib.auth import authenticate
from ..models import CustomUser, Doctor, Availability, Appointment

class UserCreatorFacade():
    def __init__(self, model) -> None:
        self.model = model
        
    def create_user(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.model(**validated_data)
        
        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance
