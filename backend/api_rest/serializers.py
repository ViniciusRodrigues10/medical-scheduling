from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import Profile
from rest_framework.validators import UniqueValidator
import logging

logger = logging.getLogger(__name__)

class RegisterClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {
                "required": True,
                "allow_blank": False,
                "validators": [
                    UniqueValidator(
                        queryset=User.objects.all(), message="A user with that Email already exists"
                    )
                ]
            }
        }

    def create(self, validated_data):
        logger.info("Creating user with username: %s", validated_data['username'])
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        logger.info("Password set for user: %s", validated_data['username'])
        user.save()

        cliente_group = Group.objects.get(name='Patient')
        user.groups.add(cliente_group)

        return user


class RegisterMedicoSerializer(serializers.ModelSerializer):
    crm = serializers.CharField(max_length=20, required=True)
    specialization = serializers.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'crm', 'specialization')
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {
                "required": True,
                "allow_blank": False,
                "validators": [
                    UniqueValidator(
                        queryset=User.objects.all(), message="A user with that Email already exists"
                    )
                ]
            }
        }

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        
        medico_group = Group.objects.get(name='Doctors')
        user.groups.add(medico_group)
        
        Profile.objects.create(
            user=user,
            crm=validated_data['crm'],
            specialization=validated_data['specialization'],
            is_medico=True
        )
        
        return user