from django.contrib.auth import get_user_model
from abc import ABC, abstractmethod

class UserFactory(ABC):
    @staticmethod
    @abstractmethod
    def create_user(self, email, password, **extra_fields):
        ...

    @staticmethod
    @abstractmethod
    def create_superuser(self, email, password, **extra_fields):
        ...
