from django.urls import path
from authentication import views


urlpatterns = [
    path("request-otp/", views.OTPRequestAPI.as_view(), name="request-otp"),
    path("verify-otp/", views.VerifyOTPAPI.as_view(), name="verify-otp"),
]
