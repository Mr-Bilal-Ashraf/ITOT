
from rest_framework import serializers
from .models import School, School_Admins, Scl_images, Students, Classes, Applications, User_Info

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
        exclude = ['user']

    def update(self, user):
        data = {}
        for a, b in self.validated_data.items():
            if b!= None:
                data[a] = b
        User_Info.objects.update_or_create(user=user, defaults=data)


class ser_reg_school(serializers.ModelSerializer):
    class Meta:
        model = School
        exclude = ['logo','l_key']


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
        pic_1 = self.validated_data.pop("pic1")
        pic_2 = self.validated_data.pop("pic2")
        pic_3 = self.validated_data.pop("pic3")
        if pic_1 is not None:
            Scl_images.objects.update_or_create(school=schl, text="pic1", defaults={'pic':pic_1})
        if pic_2 is not None:
            Scl_images.objects.update_or_create(school=schl, text="pic2", defaults={'pic':pic_2})
        if pic_3 is not None:
            Scl_images.objects.update_or_create(school=schl, text="pic3", defaults={'pic':pic_3})


class ser_schl_apps(serializers.Serializer):
    id = serializers.IntegerField()
    logo = serializers.ImageField()
    name = serializers.CharField(max_length=60)
    city =  serializers.CharField(max_length=30)
    app_date = serializers.DateField()


class ser_show_schl(serializers.Serializer):
    user_name = serializers.CharField(max_length=100)
    mbl_num = serializers.CharField(max_length=12, allow_null=True)
    landline = serializers.CharField(max_length=15)
    designation = serializers.CharField(max_length=25)

    name = serializers.CharField(max_length=60)
    email = serializers.EmailField(allow_null=True)
    province =  serializers.CharField(max_length=30)
    city =  serializers.CharField(max_length=30)
    tehsil =  serializers.CharField(max_length=30)
    web = serializers.URLField(allow_null=True)
    type =  serializers.IntegerField(default=0)                                       # 0 for male, 1 for female, 2 for co-education
    play_area = serializers.BooleanField(default=False)                               # false for no playarea
    status_of_property = serializers.BooleanField(default=False)                      # flase means rented
    area =  serializers.FloatField(default=0)                                         # total area of school in numbers
    total_stu =  serializers.IntegerField(default=0)
    logo = serializers.ImageField(allow_null=True)
    location = serializers.CharField(max_length=100)
    address = serializers.CharField(max_length=150)
    max_teachers = serializers.IntegerField(default=0)

    pic1 = serializers.ImageField(allow_null=True)
    pic2 = serializers.ImageField(allow_null=True)
    pic3 = serializers.ImageField(allow_null=True)
    classes = ser_reg_classes(many=True)


class ser_det_schl(serializers.Serializer):
    user_name = serializers.CharField(max_length=100)
    landline = serializers.CharField(max_length=15)
    designation = serializers.CharField(max_length=25)

    name = serializers.CharField(max_length=60)
    email = serializers.EmailField(allow_null=True)
    province =  serializers.CharField(max_length=30)
    tehsil =  serializers.CharField(max_length=30)
    city =  serializers.CharField(max_length=30)
    web = serializers.URLField(allow_null=True)
    type =  serializers.IntegerField(default=0)                                       # 0 for male, 1 for female, 2 for co-education
    play_area = serializers.BooleanField(default=False)                               # false for no playarea
    status_of_property = serializers.BooleanField(default=False)                      # flase means rented
    area =  serializers.FloatField(default=0)                                         # total area of school in numbers
    total_stu =  serializers.IntegerField(default=0)
    address = serializers.CharField(max_length=150)
    logo = serializers.ImageField(allow_null=True)

    pic1 = serializers.ImageField(allow_null=True)
    pic2 = serializers.ImageField(allow_null=True)
    pic3 = serializers.ImageField(allow_null=True)


class ser_srch_school(serializers.Serializer):
    id = serializers.IntegerField()
    logo = serializers.CharField(max_length=150,allow_blank=True)
    name = serializers.CharField(max_length=60)
    address = serializers.CharField(max_length=150)


class ser_schedules(serializers.Serializer):
    id = serializers.IntegerField()
    logo = serializers.CharField(max_length=150,allow_blank=True)
    name = serializers.CharField(max_length=60)
    address = serializers.CharField(max_length=150)
    date = serializers.DateTimeField()
