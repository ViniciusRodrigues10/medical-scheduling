from abc import ABC, abstractmethod


class ModelUserFactory(ABC):
    @staticmethod
    @abstractmethod
    def create_user(self, email, password, **extra_fields): ...

    @staticmethod
    @abstractmethod
    def create_superuser(self, email, password, **extra_fields): ...
