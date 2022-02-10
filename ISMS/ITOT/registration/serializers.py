
from dataclasses import fields
from pyexpat import model
from urllib import request
from rest_framework import serializers
from .models import School, School_Admins, Scl_images, Students, Classes, Teachers, Applications, User_Info

class ser_user(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)


class ser_log_in(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=100)


class ser_forgot_password(serializers.Serializer):
    username = serializers.CharField(max_length=150)

class ser_update_profile(serializers.ModelSerializer):
    class Meta:
        model = User_Info
        exclude = ['role','user']

    def update(self, user):
        print("**********")
        print(self.validated_data.pop('Birth_Date'))
        print("**********")
        # User_Info.objects.update_or_create(user=user, defaults={'pic':self.validated_data.pop("pic"),'DOB':self.validated_data.pop('Birth_Date'),'gender':self.validated_data.pop("gender"),'mbl_num':self.validated_data.pop("mbl_num"),"religion":self.validated_data.pop("religion")})
        pass