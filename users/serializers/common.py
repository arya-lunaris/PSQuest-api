from rest_framework import serializers
from django.contrib.auth import get_user_model, password_validation, hashers

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    password_confirmation = serializers.CharField(write_only=True, required=False, allow_blank=True)

    email = serializers.EmailField()

    def validate_email(self, value):
        if get_user_model().objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate(self, data):
        password = data.get('password')
        password_confirmation = data.get('password_confirmation')

        if password and password_confirmation:
            if password != password_confirmation:
                raise serializers.ValidationError("Passwords do not match.")
            
            password_validation.validate_password(password)
            
            data['password'] = hashers.make_password(password)
        elif password and not password_confirmation:
            raise serializers.ValidationError("Password confirmation is required.")

        return data

    def create(self, validated_data):
        validated_data.pop('password_confirmation', None)
        user = get_user_model().objects.create(**validated_data)
        return user

    def update(self, instance, validated_data):
        validated_data.pop('password_confirmation', None)

        password = validated_data.get('password', None)
        if password:
            validated_data['password'] = hashers.make_password(password)

        return super().update(instance, validated_data)

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'bio', 'is_staff', 'profile_image', 'password', 'password_confirmation')

