from rest_framework import serializers
from .models import User, Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'is_active', 'date_joined']
        extra_kwargs = {
            'password': {'write_only': True},  # Ensure password is not returned in the response
        }

    def create(self, validated_data):
        # Ensure the password is hashed before saving
        user = User(
            email=validated_data['email'],
            is_active=validated_data.get('is_active', True)  # Default to active if not provided
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Only pop if the password key exists
        if 'password' in data:
            data.pop('password')  # Exclude password from representation
        return data


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        # Exclude the `user` field since it will be provided in the view, not by the user.
        exclude = ['user']
