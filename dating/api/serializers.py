from rest_framework import serializers
from .models import User
from django.contrib.auth import password_validation
from django.core import exceptions


class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(
        write_only = True,
        label = 'Password',
        style={
            'input_type': 'password',
        }
    )
    password2 = serializers.CharField(
        write_only = True,
        label = 'Confirm password',
        style={
            'input_type': 'password',
        }
    )

    class Meta:
        model = User
        fields = ('avatar', 'email', 'first_name', 'last_name', 'gender', 'password1', 'password2')
    
    def validate(self, attrs):
        password1 = attrs['password1']
        password2 = attrs['password2']

        if password1 != password2:
            raise serializers.ValidationError({"password2": "Passwords don't match"})
        
        # Using django password validators to check password field
        try:
            password_validation.validate_password(password1)
        except exceptions.ValidationError as errors:
            raise serializers.ValidationError({'password1': errors.messages})

        return attrs

    def create(self, validated_data):
        user = User(
            avatar = validated_data['avatar'],
            email = validated_data['email'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            gender = validated_data['gender'],
            is_active = True,
        )
        user.set_password(validated_data['password1'])
        user.save()

        return user