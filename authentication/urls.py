from django.urls import path
from authentication import views

from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

urlpatterns = [
    path("register/", views.RegistrationAPIView.as_view(), name="auth_register"),
    path("login/", TokenObtainPairView.as_view(), name="auth_token_obtain"),
    path("refresh/", TokenRefreshView.as_view(), name="auth_token_refresh"),
]
