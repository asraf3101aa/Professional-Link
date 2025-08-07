from rest_framework import serializers
from account.models import User
from django.contrib.auth import authenticate
from phonenumber_field.serializerfields import PhoneNumberField


class UserSerializer(serializers.Serializer):
    user_id = serializers.UUIDField(read_only=True)
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    contact_number = PhoneNumberField(required=True)
    full_name = serializers.CharField(required=True, max_length=50)
    company_name = serializers.CharField(required=True, max_length=100)
    address = serializers.CharField(required=True, max_length=100)
    industry = serializers.CharField(required=True, max_length=100)

    def validate_email(self, value):
        user = getattr(self, 'instance', None)
        if User.objects.filter(email=value).exclude(pk=getattr(user, 'pk', None)).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def validate_contact_number(self, value):
        user = getattr(self, 'instance', None)
        if User.objects.filter(contact_number=value).exclude(pk=getattr(user, 'pk', None)).exists():
            raise serializers.ValidationError("This contact number is already in use.")
        return value

    def validate_username(self, value):
        user = getattr(self, 'instance', None)
        if User.objects.filter(username=value).exclude(pk=getattr(user, 'pk', None)).exists():
            raise serializers.ValidationError("This username is already in use.")
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError({
                'username': ['Invalid username or password.'],
                'password': ['Invalid username or password.']
            })

        attrs['user'] = user
        return attrs
