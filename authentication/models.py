from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from core.models import City, State


class UserManager(BaseUserManager):
    def create_user(self, phone_number: int, full_name: str, password: str, role: str = "customer"):
        user = self.model(phone_number=phone_number, full_name=full_name, role=role)
        user.set_password(password)
        user.save()

    def create_superuser(self, phone_number: int, full_name: str, password: str, role: str = "admin"):
        user = self.create_user(phone_number, full_name, password, role)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.BigIntegerField(db_index=True, unique=True)
    full_name = models.CharField(max_length=128, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(max_length=128, default="user")
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "phone_number"

    objects = UserManager()

    def __str__(self):
        return str(self.phone_number)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile_images", blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    pincode = models.BigIntegerField(blank=True, null=True)
    upi_id = models.CharField(max_length=128, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class LoginOTP(models.Model):
    phone_number = models.BigIntegerField(db_index=True, unique=True)
    otp = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user
