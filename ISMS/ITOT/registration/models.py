from pyexpat import model
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User 


class School(models.Model):
    name = models.CharField(max_length=60)
    email = models.EmailField(blank=True, null= True)
    province =  models.CharField(max_length=30)
    city =  models.CharField(max_length=30)
    tehsil =  models.CharField(max_length=30)
    web = models.URLField(max_length=100, blank=True, null=True)
    type =  models.IntegerField()                                       # 0 for male, 1 for female, 2 for co-education
    play_area = models.BooleanField(default=False)                      # false for no playarea
    status_of_property = models.BooleanField(default=False)             # flase means rented
    area =  models.FloatField()                                         # total area of school in numbers
    total_stu =  models.IntegerField()
    logo = models.ImageField(upload_to="scl_logos/", blank=True, null=True)
    location = models.CharField(max_length=100)
    address = models.CharField(max_length=150)
    max_teachers = models.IntegerField()
    reg_teachers = models.IntegerField()
    key = models.CharField(max_length=15)


class Scl_images(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)         # F.K to images table, save images of the school
    pic = models.ImageField(upload_to="scl_images/", blank=True, null=True)


class Classes(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    max_stu = models.IntegerField()
    reg_stu = models.IntegerField()
    fee = models.IntegerField()



class Teachers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    classes = models.ManyToManyField(Classes)


class Applications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True)
    school = models.OneToOneField(School, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teachers, on_delete= models.CASCADE, null=True, blank=True)
    class_name = models.ForeignKey(Classes, on_delete=models.CASCADE, null=True, blank=True)
    role = models.IntegerField()                                # 0 => school, 1  => teacher, 2 => student
    status = models.IntegerField()                              # 0 => pending, 1 => approved, 2 => rejected


class User_Info(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    pic = models.ImageField(upload_to="user_pics/", blank=True, null=True)
    DOB = models.DateField()
    gender = models.BooleanField(default=True)                           #true means "male" OR false means "female"
    mbl_num = models.CharField(max_length=12, null=True, blank=True)
    religion = models.CharField(max_length=20)
    role = models.IntegerField()                                 # 0 => user, 1 => student, 2 => teacher, 3 => admin
    Con_code = models.CharField(max_length=6, null=True, blank=True)


class School_Admins(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    school = models.OneToOneField(School, on_delete=models.CASCADE)
    landline = models.CharField(max_length=15)
    designation = models.CharField(max_length=25)

    
class Students(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    G_ID = models.CharField(max_length=20, null=True, blank=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    class_name = models.ForeignKey(Classes, on_delete=models.CASCADE)
    section = models.CharField(max_length=30, blank=True, null=True)
    roll_num = models.CharField(max_length=3)
    registered_by = models.ForeignKey(Teachers)
    