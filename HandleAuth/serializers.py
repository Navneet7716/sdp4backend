
from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from rest_framework.exceptions import AuthenticationFailed
from . import google
from .register import register_social_user
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):

    email = serializers.EmailField(max_length=255,required=False)
    username = serializers.CharField(max_length=255,required=False)
    password = serializers.CharField(max_length=128, write_only=True, required=False)
    tokens = serializers.CharField(max_length=255, read_only=True, required=False)
    refresh = serializers.CharField(max_length=255, read_only=True, required=False)
    access = serializers.CharField(max_length=255, read_only=True, required=False)
    # user_id = serializers.IntegerField(required=False)

    def validate(self, data):
        print( "DATA ::",  data)
        provider = 'email'
        email = data.get('email', None)
        password = data.get('password', None)

        filtered_user_by_email = User.objects.filter(email=email)
        print("filtered_user_by_email: ", filtered_user_by_email)

        if filtered_user_by_email.exists():
            print("PROVIDER NAME: ", filtered_user_by_email[0].auth_provider)
            if provider == filtered_user_by_email[0].auth_provider or filtered_user_by_email[0].auth_provider == None:
                print("EMAIL :: ", email)
                print("PASS :: ", password)
                user = authenticate(email=email, password=password)

                print("USER :: ", user.username)

                if user == None:
                    raise Exception(
                        'A user with this email and password is not found.'
                    )
                try:

                    jwt_token = RefreshToken.for_user(user)
                    print("JWT_TOKEN ", jwt_token.access_token)
                except Exception as e:
                    print(e)

                return {
                        "refresh" : str(jwt_token),
                        "access": str(jwt_token.access_token),
                        "username" : user.username
                }
            else:
                raise AuthenticationFailed(
                    detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

        else:
            raise Exception(
                'A user with this email and password is not found.'
            )




class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):

        user_data = google.Google.validate(auth_token)

        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )

        if user_data['aud'] != settings.GOOGLE_CLIENT_ID:

            raise AuthenticationFailed('oops, who are you?')

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = 'google'

        return register_social_user(
            provider=provider, user_id=user_id, email=email, name=name)
