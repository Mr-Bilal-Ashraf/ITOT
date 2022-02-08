import email
from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from .models import School, School_Admins, Scl_images, Students, Classes, Teachers, Applications, User_Info

class ser_user(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)


class ser_log_in(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=100)


class ser_conf_code(serializers.Serializer):
    code = serializers.CharField(max_length=150)




