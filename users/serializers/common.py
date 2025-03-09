from django.contrib.auth import get_user_model, password_validation
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    password_confirmation = serializers.CharField(write_only=True, required=False, allow_blank=True)
    email = serializers.EmailField()

    def validate_email(self, value):
        if self.instance and value != self.instance.email and get_user_model().objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate(self, data):
        password = data.get("password")
        password_confirmation = data.pop("password_confirmation", None)

        if password:
            if password != password_confirmation:
                raise serializers.ValidationError("Passwords do not match.")
            password_validation.validate_password(password)

        return data 

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = get_user_model().objects.create(**validated_data)
        if password:
            user.set_password(password)  
            user.save()
        return user

    def update(self, instance, validated_data):
        validated_data.pop("password_confirmation", None)
        password = validated_data.pop("password", None)

        if password:
            instance.set_password(password)  
            instance.save()

        return super().update(instance, validated_data)

    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email", "bio", "is_staff", "profile_image", "password", "password_confirmation")


