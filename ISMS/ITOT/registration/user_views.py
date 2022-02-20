from django.shortcuts import render
from django.contrib.sessions.models import Session

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib import auth
from random import randint
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from .views import get_user_from_session, email_reset_password, remove_all_sessions


from .models import ConfCode, User_Info
from .serializers import ser_update_profile, ser_user, ser_log_in, ser_forgot_password


@api_view(['POST'])
def sign_up(request):
    result = {"username":1,"email":1}
    data = ser_user(data = request.data)
    if data.is_valid():
        data = data.data
        if User.objects.filter(username=data["username"]).exists():
            result["username"] = 0                                                      #username already exists
        if User.objects.filter(email=data["email"]).exists():
            result["email"] = 0                                                         #email already exists

        if result["username"] == 1 and result["email"] == 1:
            user = User.objects.create_user(username=data["username"], email=data["email"], password=data["password"], is_active=False)
            user.save()
            code = randint(111111,999999)
            a = ConfCode.objects.create(user=user, Con_code = code)
            a.save()
            b = User_Info.objects.create(user=user)
            b.save()
            # html_message = render_to_string('registration/Conf_Email.html', {'username':data["username"], "link": f"http://localhost:8000/reg/{user.id}/conf/code/{code}/"})
            # plain_message = strip_tags(html_message)
            # from_email = "From <mr.bilal2066@gmail.com>"
            # to_email = data["email"]
            # send_mail("Email Confirmation...", plain_message, from_email, [to_email], html_message= html_message) 
            result["status"] = 1                                                           # account created succesfully
        else:
            if result["email"]==0:
                user = User.objects.get(email=data["email"])
                if user.is_active:                                                              #account already exist and activated
                    result["status"] = 0                                                        #try logging in OR reset password
                else:
                    code = randint(111111,999999)
                    a = ConfCode.objects.update_or_create(user=user, defaults={"Con_code":code})            
                    # html_message = render_to_string('registration/Conf_Email.html', {'username':data["username"], "link": f"http://localhost:8000/reg/{user.id}/conf/code/{code}/"})
                    # plain_message = strip_tags(html_message)
                    # from_email = "From <mr.bilal2066@gmail.com>"
                    # to_email = data["email"]
                    # send_mail("Email Confirmation...", plain_message, from_email, [to_email], html_message= html_message)

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
    print(request.COOKIES)
    data = ser_log_in(data=request.data)
    if data.is_valid():
        data = data.data
        username = data["username"].lower()
        password = data["password"]
        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            if user.user_info.logged_ins < 2:
                auth.login(request, user)
                # user.user_info.logged_ins += 1
                # user.user_info.save()
                
                return Response({'status': 1, "sessionid":request.session.session_key, "role": user.user_info.role})               #logined
            else:
                return Response({'status': 3})                   # user is logged in at more than two places
        else:
            return Response({'status': 0})               #not activated OR user not found. check your email,username and password
    else:
        return Response({'status': 2})                   #given data has problems


@api_view(['POST'])
def sign_out(request):
    try:
        user = get_user_from_session(request.data["sessionid"])
        if user is not None:
            Session.objects.get(session_key=request.data["sessionid"]).delete()             # to log out from only the where the request came from  
            # user.user_info.logged_ins -= 1
            # user.user_info.save()
            return Response({'status':1})                    #logout
        else:
            return Response({'status':0})
    except:
        return Response({'status':0})                     #error


@api_view(['POST'])
def sign_out_all(request):
    try:
        user = get_user_from_session(request.data["sessionid"])
        if user is not None:
            remove_all_sessions(user.id)                                                  # logout the user from all computers
            user.user_info.logged_ins = 0
            user.user_info.save()
            return Response({'status':1})                    #logout
        else:
            return Response({'status':0})
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
        user = get_user_from_session(request.data["sessionid"])
        if user is not None:
            if user.check_password(data["username"]):
                user.set_password(data["password"])
                user.save()
                return Response({'status':1})                                                                           #password updated
            else:
                return Response({'status':0})                                                                           #wrong password
        else:
            return Response({'status':0})
    else:
        return Response({'status':2})                                                                               #invalid data


# @parser_classes([MultiPartParser, FormParser])
@api_view(['POST'])
def update_profile(request):
    name=request.data['name']
    father_name=request.data['father_name']
    user = get_user_from_session(request.data["sessionid"])
    if user is not None:
        data = ser_update_profile(data=request.data)
        if data.is_valid():
            data.update(user)
            user.first_name = name
            user.last_name = father_name
            user.save()
            return Response({'status':1})
        else:
            return Response({'status':0})
    else:
        return Response({'is_logged_in':0})


@api_view(['POST'])
def is_complete(request):
    user = get_user_from_session(request.data["sessionid"])
    if user is not None:
        if user.user_info.mbl_num != None:
            return Response({'status':1})
    else:
        return Response({'is_logged_in':0})


@api_view(['POST'])
def get_profile(request):
    print(request.COOKIES)
    user = get_user_from_session(request.data["sessionid"])
    if user is not None:
        if user.is_authenticated:
            data = {}
            data["name"]=user.first_name
            data["father_name"]=user.last_name
            ser_user_info = ser_update_profile(User_Info.objects.get(user=user))
            data["info"] = ser_user_info.data
            return Response(data)
        else:
            return Response({'is_logged_in':0})
    else:
        return Response({'is_logged_in':0})


