import email
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
import json

from .models import User
from django.contrib.auth import logout
from rest_framework import status

from rest_framework.permissions import IsAuthenticated

from .serializers import UserLoginSerializer, UserSerializer, UserRegistrationSerializer, GoogleSocialAuthSerializer


class UserRegistrationView(CreateAPIView):

    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        status_code = status.HTTP_201_CREATED
        response = {
            'success': 'True',
            'status code': status_code,
            'message': 'User registered  successfully',
        }

        return Response(response, status=status_code)


class UserLoginView(RetrieveAPIView):

    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def get(self, request):
        return Response({'Hello': 'User'}, status.HTTP_200_OK)

    def post(self, request):

        try:

            print("REQUEST DATA ", request.data)
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=False)
            print("SERIALIZER DATA :: ", serializer.data)
            d = {'email' : request.data.get("email"), 'username' : serializer.data.get("username") }
            response = {
                'success': 'True',
                'status code': status.HTTP_200_OK,
                'message': 'User logged in  successfully',
                'access' : serializer.data.get('access'),
                 'data' : d
            }
            status_code = status.HTTP_200_OK

            return JsonResponse(response, status=status_code)
        except Exception as e:
            print(e)
            status_code = status.HTTP_404_NOT_FOUND
            return Response({'error': str(e), 'status': 0}, status_code)


class UserLogoutView(RetrieveAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request):
        logout(request)
        return Response({'message': 'Logout Successfull'}, status=status.HTTP_200_OK)


class GoogleSocialAuthView(GenericAPIView):
    permission_classes = (AllowAny,)

    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        """

        POST with "auth_token"

        Send an idtoken as from google to get user information

        """
        try:

            # print('running')
            serializer = self.serializer_class(data=request.data)
            # print('after serializer')
            serializer.is_valid(raise_exception=True)
            data = ((serializer.validated_data))
            data['status'] = 1
            print(data)
            # print('completed auth')
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)

            return Response({'error': str(e), 'status': 0})
