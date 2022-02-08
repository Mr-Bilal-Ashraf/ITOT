from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib import auth
from random import randint
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail

from .models import ConfCode
from .serializers import ser_user, ser_log_in


@api_view(['POST'])
def sign_up(request):
    result = {"username":0,"email":0}
    data = ser_user(data = request.data)
    if data.is_valid():
        data = data.data
        if User.objects.filter(username=data["username"]).exists():
            result["username"] = 1
        if User.objects.filter(email=data["email"]).exists():
            result["email"] = 1
        if result["username"] == 0 and result["email"] == 0:
            user = User.objects.create_user(username=data["username"], email=data["email"], password=data["password"], is_active=False)
            user.save()
            code = randint(111111,999999)
            a = ConfCode.objects.create(user=user, Con_code = code)
            a.save()
            html_message = render_to_string('registration/Conf_Email.html', {'username':data["username"], "code": code})
            plain_message = strip_tags(html_message)
            from_email = "From <mr.bilal2066@gmail.com>"
            to_email = data["email"]
            send_mail("Email Confirmation Code", plain_message, from_email, [to_email], html_message= html_message) 
            result["status"] = 0
        else:
            result["status"] = 1
        return Response(result)
    else:
        return Response({'x': 1})


@api_view(['POST'])
def sign_in(request):
    data = ser_log_in(data=request.data)
    if data.is_valid():
        data = data.data
        username = data["username"].lower()
        password = data["password"]
        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return Response({'x': 0})               #active and login
        else:
            return Response({'x': 1})               #not activated OR user not found. check your email,username and password
    else:
        return Response({'x': 2})                   #given data has problems



















@api_view(['GET'])
def del_user(request):
    print(request.user)
    # User.objects.get(pk=6).delete()
    return Response({'a':1})


# {"username":"Muhammad Akmal","email":"itot.pk@gmail.com","password":"Aahoo622"}
