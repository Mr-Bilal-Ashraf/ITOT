
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
import random
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from .views import get_user_from_session


from .models import Applications, Students, Teachers, School, Classes, Scl_images, School_Admins
from .serializers import ser_update_profile, ser_reg_school, ser_reg_admin, ser_reg_classes
from .views import CLASSES


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
    try:
        user = get_user_from_session(request.data["sessionid"])
        if user is not None:
            schl = user.school_admins.school
            teacher_applications = schl.applications_set.all().filter(role=1, status=0).reverse()
            for a in teacher_applications:
                d = {}
                d["app_id"] = a.id
                d["name"] = a.user.first_name
                d["img"] = str(a.user.user_info.pic)
                if len(d["img"]) != 0:
                    d["img"] = "/media/"+d["img"]
                d["app_date"] = a.app_date
                data_to_send.append(d)
            return Response({"status": data_to_send})
        else:
            return Response({"is_logged_in": 0})
    except:
        return Response({"status": 0})



@api_view(['POST'])
def students_applications(request):
    data_to_send = []
    user = get_user_from_session(request.data["sessionid"])
    if user is not None:
        schl = user.school_admins.school
        student_applications = schl.applications_set.all().filter(role=2, status=0).reverse()
        for a in student_applications:
            d = {}
            d["app_id"] = a.id
            d["name"] = a.user.first_name
            d["img"] = str(a.user.user_info.pic)
            if len(d["img"]) != 0:
                d["img"] = "/media/"+d["img"]
            d["app_date"] = a.app_date
            d["class"] = a.class_name.name
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
        html_message = render_to_string('registration/sta_teacher.html', {'username':user_name, 'school':school_name, 'status':"Rejected", 'detail':detail})
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
        try:
            if teacher.teachers:
                pass
        except:
            school = appl.school
            classes = request.data["classes"]
            teacher = Teachers.objects.update_or_create(user=teacher, defaults={'school':school})[0]
            for a in classes:
                _class_ = Classes.objects.get(pk=a["class_id"])
                teacher.classes.add(_class_)
            teacher.save()
            user = teacher.user.user_info
            user.role = 2
            user.save()
            appl.status = 1
            appl.save()
            school.reg_teachers = school.reg_teachers + 1
            school.save()
            user_name = appl.user.username.title()
            school_name = school.name.title()
            detail = "You can now register students in classes assigned to you by Admin."
            html_message = render_to_string('registration/sta_teacher.html', {'username':user_name, 'school':school_name, 'status':"Approved", 'detail':detail})
            plain_message = strip_tags(html_message)
            from_email = "From <info.itotpk@gmail.com>"
            to_email = appl.user.email
            send_mail("Teacher Application Status...", plain_message, from_email, [to_email], html_message= html_message)
            return Response({"status": 1})
        else:
            return Response({'status':0})

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
def register_student(request):
    user = get_user_from_session(request.data["sessionid"])
    try:
        if user.teachers:
            pass
    except:
        return Response({"teacher": 0})
    else:
        if user is not None:
            data = ser_update_profile(data=request.data)
            if data.is_valid():
                student_profile = {}
                a = "Faisalabad~Ditta~ITOT"
                stu = User.objects.create(username=''.join(random.sample(a,len(a))),first_name=request.data["name"], last_name=request.data["father_name"])

                names = ["muhammad", "mohammad", "md", "m"]
                us = stu.first_name.split(' ')
                if us[0].lower() in names and len(us) > 1:
                    us = us[1].lower()
                else:
                    us = us[0]
                stu.username = f"{us}-{stu.date_joined.strftime('%y')}-{stu.id:03}"
                stu.save()

                student_profile["user"] = stu
                student_profile["section"] = request.data["section"]
                student_profile["roll_num"] = request.data["roll_num"]
                student_profile["registered_by"] = user.teachers
                student_profile["class_name"] = Classes.objects.get(pk=request.data["class_id"])
                student_profile["school"] = Classes.objects.get(pk=request.data["class_id"]).school
                data.update(stu)
                Students.objects.update_or_create(user=stu, defaults=student_profile)
                Applications.objects.create(user=stu,school=student_profile["school"],teacher=user.teachers,class_name=student_profile["class_name"])

                return Response({"status":1})
            else:
                return Response({"status":0})
        else:
            return Response({"is_logged_in": 0})


@api_view(['POST'])
def app_student(request):
    user = get_user_from_session(request.data["sessionid"])
    appl = Applications.objects.get(pk=request.data["app_id"])
    reg_stu = appl.class_name.reg_stu
    max_stu = appl.class_name.max_stu
    if user is not None:
        if user.school_admins.school == appl.school and  reg_stu < max_stu and appl.status != 1:
            schl_name = appl.school.name.upper().split(" ")
            schl_abbr = ""
            for a in schl_name:
                schl_abbr += a[0]
            schl_abbr = schl_abbr[:3]
            city_name = appl.school.city.split("-")[1]
            class_name = CLASSES[appl.class_name.name]
            appl.user.students.G_ID = f"{schl_abbr}-{city_name}-{class_name}-R{appl.user.id:03}"
            appl.user.students.save()
            appl.status = 1
            appl.save()
            appl.user.user_info.role = 1
            appl.user.user_info.save()
            appl.class_name.reg_stu = appl.class_name.reg_stu+1
            appl.class_name.save()
            return Response({"status":1, "reg_stu":reg_stu+1, "max_stu":max_stu})
        else:
            return Response({"status":0, "reg_stu":reg_stu, "max_stu":max_stu})
    else:
        return Response({"is_logged_in": 0})


@api_view(['POST'])
def rej_student(request):
    user = get_user_from_session(request.data["sessionid"])
    appl = Applications.objects.get(pk=request.data["app_id"])
    if user is not None and user.school_admins.school == appl.school:
        appl.user.delete()
        return Response({'status': 1})
    else:
        return Response({"is_logged_in": 0})


@api_view(['POST'])
def validate_student(request):
    G_ID = request.data["G_ID"]
    user = request.data["username"].lower()
    try:
        stu = User.objects.get(username=user).students
    except:
        return Response({"status": 2})                              # student not registered
    else:
        if stu.G_ID.lower() == G_ID.lower():
            return Response({"status": 1})
        else:
            return Response({"status": 0})


@api_view(['POST'])
def activate_student(request):
    user = request.data["username"].lower()
    stu = ""
    try:
        user = User.objects.get(username=user)
        stu = user.students
    except:
        return Response({"status": 2})                              # student not registered
    else:
        if stu.G_ID:
            password = request.data["password"]
            user.set_password(password)
            return Response({"status": 1})                          # password set
        else:
            return Response({"status": 0})                          # student not approved









@api_view(['POST'])
def yahoo(request):
    user = get_user_from_session(request.data["sessionid"])
    if user is not None:
        pass
    else:
        return Response({"is_logged_in": 0})
