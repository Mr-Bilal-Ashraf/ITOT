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
from .views import get_user_from_session


from .models import Applications, Teachers, User_Info, School, Classes
from .serializers import ser_update_profile, ser_user, ser_log_in, ser_forgot_password


@api_view(['POST'])
def register_teacher(request):
    data = {"max_teachers": 1}
    schl = School.objects.get(pk=request.data["schl_id"])
    user = get_user_from_session(request.data["sessionid"])

    if user is not None:
        data["role"] = user.user_info.role
        data["applications"] = len(
            Applications.objects.filter(user=user, school=schl, role=1))
        if schl.reg_teachers >= schl.max_teachers:
            data["max_teachers"] = 0

        if data["role"] == 0 and data["max_teachers"] == 1 and data["applications"] == 0:
            Applications.objects.create(user=user, school=schl, role=1)
            return Response({"status": 1})
        else:
            return Response(data)
    else:
        return Response({"is_logged_in": 0})


@api_view(['POST'])
def teachers_applications(request):
    data_to_send = []
    user = get_user_from_session(request.data["sessionid"])
    if user is not None:
        schl = user.school_admins.school
        teacher_applications = schl.applications_set.all().filter(role=1)
        for a in teacher_applications:
            d = {}
            d["app_id"] = a.id
            d["name"] = a.user.first_name
            d["img"] = str(a.user.user_info.pic)
            if len(d["img"]) != 0:
                d["img"] = "/media/"+d["img"]
            d["app_date"] = a.app_date
            data_to_send.append(d)
        return Response({"data": data_to_send})
    else:
        return Response({"is_logged_in": 0})


@api_view(['POST'])
def reject_teacher_application(request):
    user = get_user_from_session(request.data["sessionid"])
    if user is not None:
        appl = Applications.objects.get(pk=request.data["app_id"])
        appl.delete()
        user_name = appl.user.username.title()
        school_name = appl.school.name.title()
        detail = "You can reApply for the role of Teacher in any school, but it is a good practice to first contact with the school Admin."
        html_message = render_to_string('registration/rej_teacher.html', {'username':user_name, 'school':school_name, 'status':"Rejected", 'detail':detail})
        plain_message = strip_tags(html_message)
        from_email = "From <info.itotpk@gmail.com>"
        to_email = appl.user.email
        send_mail("Teacher Application Status...", plain_message, from_email, [to_email], html_message= html_message)
        return Response({"status": 1})
    else:
        return Response({"is_logged_in": 0})


@api_view(['POST'])
def approve_teacher_application(request):
    user = get_user_from_session(request.data["sessionid"])
    if user is not None:
        appl = Applications.objects.get(pk=request.data["app_id"])
        teacher = appl.user
        if teacher.teachers:
            return Response({'status':0})
        else:
            school = appl.school
            classes = request.data["classes"]
            teacher = Teachers.objects.update_or_create(user=teacher, defaults={'school':school})[0]
            teacher
            for a in classes:
                _class_ = Classes.objects.get(pk=a["class_id"])
                teacher.classes.add(_class_)
            teacher.save()
            user_name = appl.user.username.title()
            school_name = school.name.title()
            detail = "You can now register students in classes assigned to you by Admin."
            html_message = render_to_string('registration/rej_teacher.html', {'username':user_name, 'school':school_name, 'status':"Approved", 'detail':detail})
            plain_message = strip_tags(html_message)
            from_email = "From <info.itotpk@gmail.com>"
            to_email = appl.user.email
            send_mail("Teacher Application Status...", plain_message, from_email, [to_email], html_message= html_message)
            return Response({"status": 1})
    else:
        return Response({"is_logged_in": 0})


@api_view(['POST'])
def my_classes(request):
    user = get_user_from_session(request.data["sessionid"])
    if user is not None:
        classes = user.school_admins.school.classes_set.all().values('name','id')
        data = []
        for a in classes:
            data.append({'class_id':a["id"],'name':a["name"]})
        return Response({'classes':data})
    else:
        return Response({"is_logged_in": 0})





@api_view(['POST'])
def yahoo(request):
    user = get_user_from_session(request.data["sessionid"])
    if user is not None:
        pass
    else:
        return Response({"is_logged_in": 0})