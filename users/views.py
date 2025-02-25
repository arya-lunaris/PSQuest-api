from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers.common import UserSerializer

# Create your views here.
class RegisterView(APIView):

    def post(self, request):
        serialized_user = UserSerializer(data=request.data)
        if serialized_user.is_valid():
            serialized_user.save()
            return Response(serialized_user.data, 201)
        return Response(serialized_user.errors, 422)
    

class LoginView(APIView):

    def post(self, request):
        return Response('HIT LOGIN ROUTE')