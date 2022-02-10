from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib import auth
from random import randint
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail


import sys
from PIL import Image, ImageOps
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


from .models import ConfCode, User_Info
from .serializers import ser_update_profile, ser_user, ser_log_in, ser_forgot_password


@api_view(['POST'])
def sign_up(request):
    result = {"username":0,"email":0}
    data = ser_user(data = request.data)
    if data.is_valid():
        data = data.data
        if User.objects.filter(username=data["username"]).exists():
            result["username"] = 1                                                      #username already exists
        if User.objects.filter(email=data["email"]).exists():
            result["email"] = 1                                                         #email already exists




        if result["username"] == 0 and result["email"] == 0:
            user = User.objects.create_user(username=data["username"], email=data["email"], password=data["password"], is_active=False)
            user.save()
            code = randint(111111,999999)
            a = ConfCode.objects.create(user=user, Con_code = code)
            a.save()
            b = User_Info.objects.create(user=user)
            b.save()
            html_message = render_to_string('registration/Conf_Email.html', {'username':data["username"], "link": f"http://localhost:8000/reg/{user.id}/conf/code/{code}/"})
            plain_message = strip_tags(html_message)
            from_email = "From <mr.bilal2066@gmail.com>"
            to_email = data["email"]
            send_mail("Email Confirmation...", plain_message, from_email, [to_email], html_message= html_message) 
            result["status"] = 0                                                           # account created succesfully
        else:
            if result["email"]==1:
                user = User.objects.get(email=data["email"])
                if user.is_active:                                                              #account already exist and activated
                    result["status"] = 1                                                        #try logging in OR reset password
                else:
                    code = randint(111111,999999)
                    a = ConfCode.objects.update_or_create(user=user, defaults={"Con_code":code})            
                    html_message = render_to_string('registration/Conf_Email.html', {'username':data["username"], "link": f"http://localhost:8000/reg/{user.id}/conf/code/{code}/"})
                    plain_message = strip_tags(html_message)
                    from_email = "From <mr.bilal2066@gmail.com>"
                    to_email = data["email"]
                    send_mail("Email Confirmation...", plain_message, from_email, [to_email], html_message= html_message)

                    result["status"] = 2                                                        #ask for confirmation code, ConfCode sent to email
            else:
                result["status"] = 3                                                            #username already used
        return Response(result)
    else:
        return Response({'x': 1})                                                               #data not valid


@api_view(['GET'])
def confirm_code(request,id,code):
    if User.objects.filter(pk=id).exists():
        user = User.objects.get(pk=id)
        if code == user.confcode.Con_code:
            user.is_active = True
            user.save()
            user.confcode.delete()
        return Response({'status':0})                                                           #account activated successfully
    else:
        return Response({'status':1})                                                           #user does not exist


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
            return Response({'status': 0, 'role':request.user.user_info.role})               #logined
        else:
            return Response({'status': 1})               #not activated OR user not found. check your email,username and password
    else:
        return Response({'status': 2})                   #given data has problems


@api_view(['GET'])
def sign_out(request):
    try:
        auth.logout(request)
        return Response({'status':1})                    #logout
    except:
        return Response({'status':0})                     #error


@api_view(['POST'])
def forgot_password(request):
    data = ser_forgot_password(data=request.data)
    if data.is_valid():
        data = data.data
        if User.objects.filter(username=data["username"].lower()).exists():
            email_reset_password(User.objects.get(username=data["username"].lower()))
            return Response({"status":1})                                                                       #password reset email sent
        elif User.objects.filter(email=data["username"]).exists():
            email_reset_password(User.objects.get(email=data["username"].lower()))
            return Response({"status":1})
        else:
            return Response({"status":0})                                                                       # user with this email OR username doesn't exist
    else:
        return Response({"status":2})                                                                           #invalid data


def email_reset_password(user):
    code = randint(111111,999999)
    b = randint(11,99)
    a = ConfCode.objects.update_or_create(user=user, defaults={"Con_code":code})
    html_message = render_to_string('registration/for_pas_email.html', {"code": f"{code}#{b}#{user.id}"})
    plain_message = strip_tags(html_message)
    from_email = "From <mr.bilal2066@gmail.com>"
    to_email = user.email
    send_mail("Reset Your Password...", plain_message, from_email, [to_email], html_message= html_message)


@api_view(['POST'])
def forgot_password_reset(request):
    data = ser_log_in(data=request.data)
    if data.is_valid():
        data = data.data
        data_arr = data["username"].split("#")
        if User.objects.filter(pk=data_arr[2]).exists() and len(data_arr) == 3:
            user = User.objects.get(pk=data_arr[2])
            if data_arr[0] == user.confcode.Con_code:
                user.set_password(data["password"])
                user.save()
                user.confcode.delete()
                return Response({"status":1})                                                                       #password reset
            else:
                return Response({"status":0})                                                                       #wrong conf code
        else:
                return Response({"status":2})                                                                       #user does not exist
    else:
        return Response({"status":3})                                                                               #invalid data


@api_view(['POST'])
def update_password(request):
    data = ser_log_in(data=request.data)
    if data.is_valid():
        data = data.data
        if request.user.check_password(data["username"]):
            request.user.set_password(data["password"])
            request.user.save()
            return Response({'status':0})                                                                           #password updated
        else:
            return Response({'status':1})                                                                           #wrong password
    else:
        return Response({'status':2})                                                                               #invalid data


# @parser_classes([MultiPartParser, FormParser])
# @api_view(['POST'])
# def update_profile(request):
#     # for x in request.data:
#     #     if request.data[x] == "null":
#     #         request.data[x] = None
#     #     if x == "profile" and request.data[x] != None:
#     #         imageTemproary = Image.open(request.data[x])
#     #         outputIoStream = BytesIO()
#     #         imageTemproary = imageTemproary.resize((150,150),Image.ANTIALIAS)
#     #         imageTemproary = ImageOps.exif_transpose(imageTemproary)
#     #         imageTemproary.save(outputIoStream , format='webp', quality=90)
#     #         outputIoStream.seek(0)
#     #         request.data[x] = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.webp" % request.data[x].name.split('.')[0], 'image/webp', sys.getsizeof(outputIoStream), None)

#     abcd = ser_update_profile(data=request.data)
#     if abcd.is_valid():
#         print(abcd.data)
#         return Response({'status':abcd.data})
#     else:
#         print(abcd.errors)
#         return Response({'status':0})


class upda(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def post(self, request, format=None):
        abcd = ser_update_profile(data=request.data)
        if abcd.is_valid():
            abcd.update(request.user)
            return Response({'status':abcd.data})
        else:
            print(abcd.errors)
            return Response({'status':0})





















@api_view(['GET'])
def check(request):
    return render(request,'registration/check.html')




@api_view(['GET'])
def del_user(request):
    print(request.user)
    # User.objects.get(pk=7).delete()
    return Response({'a':1})


# {"username":"Bilal","email":"mr.azaad622@gmail.com","password":"12345"}
