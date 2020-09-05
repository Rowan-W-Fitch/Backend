from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Beach
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from .serializers import UserSerializer, BeachSerializer
from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
from rest_framework.parsers import JSONParser
# Create your views here.


class UserRegistration(mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    parser_classes = [JSONParser]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            usr = serializer.save()
            token, created = Token.objects.get_or_create(user = usr)
            return Response({
                'token': token.key,
                'id': usr.id
            })
        else:
            raise exceptions.AuthenticationFailed("invalid data")

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CustomAuthToken(APIView):

    def post(self, request, *args, **kwargs):
        uname = request.data.get('username')
        passw = request.data.get('password')
        if not uname:
            return None

        try:
            usr = User.objects.get(username = uname)

        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("user dne")

        if not usr.check_password(passw):
            raise exceptions.AuthenticationFailed("password incorrect")

        token, created = Token.objects.get_or_create(user = usr)
        return Response({
            'token': token.key,
            'id':usr.id
        })


class CreateBeach(mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = BeachSerializer
    queryset = Beach.objects.all()
    parser_classes = [JSONParser]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            beach = serializer.save()
            return Response({
                'id': beach.id
            })
        else:
            print(serializer.errors)
            raise exceptions.AuthenticationFailed("invalid data")

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class UpdateBeach(APIView):
    def post(self, request, *args, **kwargs):

        id_no = request.data.pop('beach_id')
        if not id_no:
            return None

        try:
            beach = Beach.objects.get(id = id_no)
        except Beach.DoesNotExist:
            raise exceptions.AuthenticationFailed("beach dne")

        bch = BeachSerializer(beach, data = request.data)
        if bch.is_valid():
            bch.save()
            return Response({
                'id': beach.id
            })
        else:
            print(bch.errors)
            raise exceptions.AuthenticationFailed("invalid data")
