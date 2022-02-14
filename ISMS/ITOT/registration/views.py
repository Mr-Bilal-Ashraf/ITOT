from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib import auth
from random import randint
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail


from .models import ConfCode, User_Info, School,School_Admins,Classes, Applications, Scl_images
from .serializers import ser_logo, ser_schl_apps, ser_update_profile, ser_user, ser_log_in, ser_forgot_password, ser_reg_classes, ser_reg_school,ser_reg_admin


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
    data = ser_log_in(data=request.data)
    if data.is_valid():
        data = data.data
        username = data["username"].lower()
        password = data["password"]
        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return Response({'status': 1})               #logined
        else:
            return Response({'status': 0})               #not activated OR user not found. check your email,username and password
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
@api_view(['POST'])
def update_profile(request):
    name=request.data['name']
    father_name=request.data['father_name']
    user = request.user
    data = ser_update_profile(data=request.data)
    if data.is_valid():
        data.update(user)
        user.first_name = name
        user.last_name = father_name
        user.save()
        return Response({'status':data.data})
    else:
        return Response({'status':0})


@api_view(['GET'])
def is_complete(request):
    if request.user.user_info.mbl_num != None:
        return Response({'status':1})
    return Response({'status':0})


@api_view(['POST'])
def register_school(request):
    result = {"role":0, "admin": 0, 'status':0}
    if request.user.is_authenticated:

        result["role"] = request.user.user_info.role                                                        #ROLE 0 => user, 1 => student, 2 => teacher, 3 => admin
        result["admin"] = 1 if School_Admins.objects.filter(user=request.user) else 0                           # admin = 0 means user holds no school

        if result["admin"] == 0 and result["role"] == 0:
            ser_school = ser_reg_school(data=request.data["school"])
            ser_admin = ser_reg_admin(data=request.data["admin"])
            ser_classes = ser_reg_classes(data=request.data["classes"], many=True)
            if ser_school.is_valid() and ser_classes.is_valid() and ser_admin.is_valid():
                schl = ser_school.save()
                ser_admin.create(request.user, schl)
                for a in ser_classes.data:
                    data = {}
                    for key, value in a.items():
                        data[key] = value
                    Classes.objects.create(school=schl,name=data["name"],max_stu=data["max_stu"],fee=data["fee"])
                
                Applications.objects.create(user=request.user,school= schl,role=0)
                Scl_images.objects.create(school=schl,text="pic1")
                Scl_images.objects.create(school=schl,text="pic2")
                Scl_images.objects.create(school=schl,text="pic3")

                result["status"]=1
                return Response(result)
            else:
                return Response({'x':0})                      # data not valid
        else:
            return Response(result)                           # status 0 operation fail for school application
    else:
        return Response({'is_logged_in':0})                   # user not authenticated


@api_view(['GET'])
def show_school_applications(request):
    if request.user.is_superuser:
        data = []
        schls = Applications.objects.filter(role=0).values('school','app_date')
        for schl in schls:
            scl_obj = School.objects.get(pk=schl["school"])
            result = {'id':scl_obj.id ,'logo': scl_obj.logo, 'name': scl_obj.name, 'city': scl_obj.city, 'app_date': schl["app_date"]}
            data.append(result)
        data = ser_schl_apps(data,many=True)
        return Response(data.data)
    else:
        return Response({'admin':0})


@api_view(['POST'])
def show_specific_school(request):
    if request.user.is_superuser:

        pass
    else:
        return Response({'admin':0})


@api_view(['POST'])
def approve_school(request):
    pass


@api_view(['POST'])
def reject_school(request):
    if request.user.is_superuser:
        reason = request.data["reason"]
        # html_message = render_to_string('registration/Conf_Email.html', {'username':data["username"], "link": f"http://localhost:8000/reg/{user.id}/conf/code/{code}/"})
        # plain_message = strip_tags(html_message)
        # from_email = "From <mr.bilal2066@gmail.com>"
        # to_email = data["email"]
        # send_mail("Email Confirmation...", plain_message, from_email, [to_email], html_message= html_message)
    return Response({'reason': reason})


@api_view(['POST'])
def update_logo(request):
    request.data._mutable = True
    for x in request.data:
        if request.data[x] == "null":
            request.data[x] = None

    data = ser_logo(data=request.data)
    if data.is_valid():
        data.update(request.user)
        return Response({"updated":1})
    else:
        # return Response({"updated":0})
        return Response({"updated":data.errors})
        

@api_view(['GET'])
def get_profile(request):
    if request.user.is_authenticated:
        user = request.user
        data = {}
        data["name"]=user.first_name
        data["father_name"]=user.last_name
        ser_user_info = ser_update_profile(User_Info.objects.get(user=user))
        data["info"] = ser_user_info.data
        return Response(data)
    else:
        return Response({'is_logged_in':0})















@api_view(['GET'])
def check(request):
    return render(request,'registration/check.html')


@api_view(['GET'])
def del_user(request):
    print(request.user)
    # User.objects.get(pk=7).delete()
    return Response({'a':1})


# {"username":"Bilal","email":"mr.azaad622@gmail.com","password":"12345"}
