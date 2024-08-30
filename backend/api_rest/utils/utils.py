from rest_framework import serializers


def serializer_create_user(self, validated_data):
    password = validated_data.pop("password", None)
    instance = self.model(**validated_data)

    if password is not None:
        instance.set_password(password)

    instance.save()
    return instance


def serializer_evaluates_whether_email_is_in_use(self, email):
    if (
        self.class_user.objects.exclude(pk=self.user.id_user)
        .filter(email=email)
        .exists()
    ):
        raise serializers.ValidationError("This email is already in use")

    return email
