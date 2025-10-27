from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import CustomUser
from .serializers import UserSerializer


class GetUserView(generics.GenericAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            user = CustomUser.objects.get(id=request.user.id)
            return Response(UserSerializer(user).data, status=200)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=404)
