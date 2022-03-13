import email
from rest_framework import serializers
from django.contrib.auth import get_user_model
from users.email import send_activation_email
from users.tokens import account_activation_token
from rest_framework.exceptions import PermissionDenied

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            password=validated_data["password"],
        )
        user.is_active = False
        send_activation_email(user)
        user.save()
        return user

    class Meta:
        model = UserModel
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
        )


class AccountRestorationRequestSerializer(serializers.Serializer):
    email = serializers.CharField()


class AccountRestorationSerializer(serializers.Serializer):
    uid = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)


class GrantStaffSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        instance.is_staff = validated_data.get(validated_data, instance.is_staff)
        instance.save()
        return instance

    class Meta:
        model = UserModel
        fields = ("id", "username", "is_staff")
        extra_kwargs = {"id": {"read_only": True}, "username": {"read_only": True}}
