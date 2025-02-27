from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated, ValidationError
from django.contrib.auth import get_user_model
import jwt
from .serializers.common import UserSerializer
from django.conf import settings
from datetime import timedelta
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone


# Create your views here.
class SignupView(APIView):

    def post(self, request):
        serialized_user = UserSerializer(data=request.data)
        if serialized_user.is_valid():
            serialized_user.save()
            return Response(serialized_user.data, 201)
        return Response(serialized_user.errors, 422)
    

class LoginView(APIView):
    def post(self, request):
        identifier = request.data.get('identifier') 
        password = request.data.get('password')

        try:
            User = get_user_model()
            
            user = User.objects.filter(username=identifier).first() or User.objects.filter(email=identifier).first()

            if not user:
                raise NotAuthenticated('Invalid credentials')

            if not user.check_password(password):
                raise ValidationError('Incorrect password')

            exp_date = timezone.now() + timedelta(days=7)

            token = jwt.encode(
                payload={
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'is_admin': user.is_staff,
                        'email': user.email
                    },
                    'exp': int(exp_date.timestamp())  
                },
                key=settings.SECRET_KEY,
                algorithm='HS256'
            )

            return Response({'message': 'Login was successful', 'token': token})

        except (ValidationError, NotAuthenticated) as e:
            print(e)
            raise NotAuthenticated('Invalid credentials')

 

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  
        serializer = UserSerializer(user)  
        return Response(serializer.data, status=200)

    def put(self, request):
        user = request.user  

        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=200)

        return Response(serializer.errors, status=400)