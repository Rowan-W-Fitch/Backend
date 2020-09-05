from rest_framework import serializers
from .models import Beach
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        usr = self.Meta.model(**validated_data)
        if password:
            usr.set_password(password)
        usr.save()
        return usr

class BeachSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beach
        fields = "__all__"

    def create(self, validated_data):
        beach = self.Meta.model(**validated_data)
        beach.save()
        return beach
