from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated, ValidationError
from django.contrib.auth import get_user_model
import jwt
from .serializers.common import UserSerializer
from django.conf import settings
from datetime import datetime, timedelta


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
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            User = get_user_model()
            user = User.objects.get(username=username)

            if not user.check_password(password):
                raise ValidationError('Passwords do not match')
            
            exp_date = datetime.now() + timedelta(days=1)
            

            token = jwt.encode(
                payload={
                    'user': {
                        'id': user.id,
                        'username': user.profile_image,
                        'is_admin': user.is_staff
                    },
                    'exp': int(exp_date.strftime('%s'))
                },
                key=settings.SECRET_KEY,
                algorithm='HS256'
            )

            return Response({ 'message': 'Login was successful', 'token': token})

        except (User.DoesNotExist, ValidationError) as e:
            print(e)
            raise NotAuthenticated('Invalid credentials')
 
        