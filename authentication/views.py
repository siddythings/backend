from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from authentication.serializers import RegistrationSerializer

from authentication.models import User


class RegistrationAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    queryset = User.objects.all()
