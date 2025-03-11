from rest_framework import serializers
from django.contrib.auth import authenticate
from apps.users.models import User
from django.core.exceptions import ObjectDoesNotExist


class LoginSerializer(serializers.Serializer):
    username = serializers.EmailField(required=True, allow_blank=False)
    password = serializers.CharField(
        required=True, allow_blank=False, write_only=True, min_length=8
    )

    def validate(self, attrs):
        user: User = authenticate(attrs.get("username"), attrs.get("password"))
        if user is None:
            raise serializers.ValidationError(
                "Unable to log in with provided credentials."
            )
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")
        return user


class SetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField(write_only=True)
    pass1 = serializers.CharField(max_length=128, min_length=6, write_only=True)
    pass2 = serializers.CharField(max_length=128, min_length=6, write_only=True)

    def validate(self, data):
        if data["pass1"] != data["pass2"]:
            raise serializers.ValidationError({"password": "Password do not match"})
        return data

    def validate_token(self, value):
        try:
            self.user: User = User.objects.get(pass_token=value)
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Invalid token")
        return value

    def save(self, **kwargs):
        self.user.set_password(self.validated_data["pass1"])
        self.user.pass_token = None
        self.user.save()
        return self.user


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, allow_blank=False)

    def validate_email(self, value):
        try:
            self.user: User = User.objects.get(email=value)
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Invalid email")
        return value

    def save(self, **kwargs):
        self.user.reset_pass_token()
        return self.user
