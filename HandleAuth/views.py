import email
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
import json
import random
import string
import os

import datetime

from pdf2image import convert_from_path, convert_from_bytes
from zipfile import ZipFile
import img2pdf 
import re

from .models import User, UserFiles
from django.contrib.auth import logout
from rest_framework import status

from rest_framework.permissions import IsAuthenticated

from .serializers import UserDataSerializer, UserLoginSerializer, UserSerializer, UserRegistrationSerializer, GoogleSocialAuthSerializer

from storages.backends.s3boto3 import S3Boto3Storage


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


class UpdateData(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserDataSerializer

    def post(self, request):

        try:

            print(request.data)
            

            j = UserFiles()
            j.created_on = datetime.datetime.now()
            j.update_on = datetime.datetime.now()
            


            j.file_name = request.data['file_name']
            j.file_url = request.data['file_url']
            j.old_name = request.data['old_name']
            j.old_url = request.data['old_url']
            j.user_email =  request.data['email']
            j.file_size = request.data['file_size']
            j.file_type = request.data['file_type']

            j.save()
            return JsonResponse({"message" : "success"})

        except Exception as e:

            print(str(e) )

            return JsonResponse({"message" : "error"})


class GetUserFiles(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserDataSerializer

    def get(self, request, email):
        try:

            plist = list(UserFiles.objects.values().filter(
                user_email=email).order_by('-created_on'))

            response = {
                'success': 'true',
                 'message': 'User Post fetched successfully',
                 'data': plist
             }    
            status_code = status.HTTP_200_OK
            return Response(response, status=status_code)         



        except Exception as e:

            response = {
                'success': 'false',
                 'message': 'error',
                 'data': []
             }  

            status_code = status.HTTP_200_OK

            print(str(e))
            return Response(response, status=status_code)         





        