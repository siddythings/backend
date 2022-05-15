from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_400_BAD_REQUEST

from authentication.models import User, Profile, LoginOTP

from authentication.serializers import UserLoginSerializer

from datetime import datetime, timedelta

from authentication.utils import generate_OTP
from core.utils import get_object_or_error


class OTPRequestAPI(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        phone_number = request.data.get("phone_number")
        if not phone_number:
            return Response({"message": "Phone number is required"}, status=HTTP_400_BAD_REQUEST)

        user = User.objects.get_or_create(phone_number=phone_number)
        if user[1]:
            Profile.objects.create(user=user[0])
        # Check if user is deactivated
        elif not user[1] and user[0].is_active == False:
            return Response({"detail": "User is not active"}, status=HTTP_400_BAD_REQUEST)

        otp = generate_OTP()

        # Delete all previous OTPs and Create a new one
        LoginOTP.objects.filter(user=user[0]).delete()
        LoginOTP.objects.create(user=user[0], otp=otp)

        # FIXME: Remove `test_otp` in production
        return Response({"status": "OTP sent and will be acceptable for 15 minutes only", "test_otp": otp})


class VerifyOTPAPI(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        phone_number = request.data.get("phone_number")
        otp = request.data.get("otp")

        if not (phone_number and otp):
            return Response({"message": "Phone number and OTP are required"}, status=HTTP_400_BAD_REQUEST)

        user = get_object_or_error(User, phone_number=phone_number, error_message="Request OTP first")

        try:
            LoginOTP.objects.get(user=user, otp=otp, created_at__gte=datetime.now() - timedelta(minutes=15))
        except LoginOTP.DoesNotExist:
            return Response({"message": "OTP does not match"}, status=HTTP_400_BAD_REQUEST)

        user.is_verified = True
        user.save()

        serializer = self.serializer_class(data={"phone_number": phone_number})
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)
