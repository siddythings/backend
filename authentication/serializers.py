from rest_framework import serializers

from authentication.models import User

from core.utils import get_object_or_error


class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=255, required=False)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        phone_number = data.get("phone_number", None)

        if phone_number is None:
            raise serializers.ValidationError("An email or username or phonenumber is required to log in.")

        # authenticate using phone number or username or email
        user = get_object_or_error(
            User, phone_number=phone_number, is_verified=True, error_message="User does not exist."
        )

        return {"token": user.token}
