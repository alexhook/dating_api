from rest_framework.generics import CreateAPIView
from .serializers import UserSerializer
from .models import User

class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer

