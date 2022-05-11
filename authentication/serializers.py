from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from authentication.models import User, Profile, LoginOTP


class RegistrationSerializer(serializers.ModelSerializer):
    phone_number = serializers.IntegerField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ("phone_number", "password", "confirm_password")

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(phone_number=validated_data["phone_number"])
        user.set_password(validated_data["password"])
        user.save()

        Profile.objects.create(user=user)

        return user
