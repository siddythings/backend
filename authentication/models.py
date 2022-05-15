from django.db import models
from django.conf import settings
import jwt
from core.models import City, State
from datetime import datetime, timedelta


class User(models.Model):
    phone_number = models.BigIntegerField(db_index=True, unique=True)
    full_name = models.CharField(max_length=128, blank=True, null=True)
    role = models.CharField(max_length=128, default="user")
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.phone_number)

    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().
        The `@property` decorator above makes this possible. `token` is called
        a "dynamic property".
        """
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(60)
        token = jwt.encode(
            {
                "uuid": str(self.uuid),
                "exp": int(dt.timestamp()),
            },
            settings.SECRET_KEY,
            algorithm="HS256",
        )

        return token


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile_images", blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, default=None)
    state = models.ForeignKey(State, on_delete=models.CASCADE, default=None)
    pincode = models.BigIntegerField(blank=True, null=True)
    upi_id = models.CharField(max_length=128, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class LoginOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user
