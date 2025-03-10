from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model
import jwt
from django.conf import settings
from datetime import timedelta
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from rest_framework import status
from .serializers.common import UserSerializer


User = get_user_model()

class SignupView(APIView):
    def post(self, request):
        serialized_user = UserSerializer(data=request.data)
        if serialized_user.is_valid():
            user = serialized_user.save()  

            exp_date = timezone.now() + timedelta(days=7)
            token = jwt.encode(
                payload={
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'is_staff': user.is_staff,
                        'email': user.email
                    },
                    'exp': int(exp_date.timestamp())  
                },
                key=settings.SECRET_KEY,
                algorithm='HS256'
            )

            return Response({
                "user": serialized_user.data,
                "token": token  
            }, status=status.HTTP_201_CREATED)

        return Response(serialized_user.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class LoginView(APIView):
    def post(self, request):
        identifier = request.data.get('identifier') 
        password = request.data.get('password')

        try:
            user = get_user_model().objects.filter(username=identifier).first() or get_user_model().objects.filter(email=identifier).first()

            if not user:
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

            if not user.check_password(password):
                return Response({'detail': 'Incorrect password'}, status=status.HTTP_401_UNAUTHORIZED)

            exp_date = timezone.now() + timedelta(days=7)
            token = jwt.encode(
                payload={
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'is_staff': user.is_staff,
                        'email': user.email
                    },
                    'exp': int(exp_date.timestamp())  
                },
                key=settings.SECRET_KEY,
                algorithm='HS256'
            )

            return Response({'message': 'Login successful', 'token': token})

        except Exception as e:
            print("Error during login:", e)
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)  
        return Response(serializer.data, status=200)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)
