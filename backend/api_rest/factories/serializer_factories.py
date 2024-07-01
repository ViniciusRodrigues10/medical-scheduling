from abc import ABC, abstractmethod


class SerializerUserFactory(ABC):
    @staticmethod
    @abstractmethod
    def create_user(self, validated_data): ...


class ValidateEmailForRegistrationFactory(ABC):
    @staticmethod
    @abstractmethod
    def evaluates_whether_email_is_in_use(self, email): ...


class ValidadeLoginFactory(ABC):
    @staticmethod
    @abstractmethod
    def validate(self): ...


class SerializerDoctorFactory(ABC):
    @staticmethod
    @abstractmethod
    def create_doctor(self, validated_data): ...

    @staticmethod
    @abstractmethod
    def update_doctor(self, instance, validated_data): ...
