
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
        data = {}
        for a, b in self.validated_data.items():
            data[a] = b
        User_Info.objects.update_or_create(user=user, defaults=data)


class ser_reg_school(serializers.ModelSerializer):
    class Meta:
        model = School
        exclude = ['logo','key']


class ser_reg_admin(serializers.ModelSerializer):
    class Meta:
        model = School_Admins
        exclude = ['user','school']

    def create(self,user,school):
        data = {}
        for key, value in self.validated_data.items():
            data[key] = value
        School_Admins.objects.create(user=user,school=school,landline=data["landline"],designation=data["designation"])


class ser_reg_classes(serializers.Serializer):

    name = serializers.CharField(max_length=30)
    max_stu = serializers.IntegerField()
    fee = serializers.IntegerField()


class ser_logo(serializers.Serializer):
    logo = serializers.ImageField(allow_null=True)
    pic1 = serializers.ImageField(allow_null=True)
    pic2 = serializers.ImageField(allow_null=True)
    pic3 = serializers.ImageField(allow_null=True)


    def update(self,user):
        schl = user.school_admins.school
        schl.logo = self.validated_data.pop("logo")
        schl.save()
        Scl_images.objects.update_or_create(school=schl, text="pic1", defaults={'pic':self.validated_data.pop("pic1")})
        Scl_images.objects.update_or_create(school=schl, text="pic2", defaults={'pic':self.validated_data.pop("pic2")})
        Scl_images.objects.update_or_create(school=schl, text="pic3", defaults={'pic':self.validated_data.pop("pic3")})

class ser_schl_apps(serializers.Serializer):
    id = serializers.IntegerField()
    logo = serializers.ImageField()
    name = serializers.CharField(max_length=60)
    city =  serializers.CharField(max_length=30)
    app_date = serializers.DateField()