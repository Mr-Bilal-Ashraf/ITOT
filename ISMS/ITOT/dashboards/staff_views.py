import pytz
from datetime import datetime
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


from registration.views import get_user_from_session, MONTHS
from registration.models import Schedule, School, Applications
from registration.serializers import ser_schedules, ser_schl_apps, ser_show_schl





#************************** Applications ********************************

@api_view(['POST'])
def show_school_applications(request):
    user = get_user_from_session(request.data["sessionid"])
    if user is not None:
        if user.user_info.role in [4,5]:
            data = []
            schls = Applications.objects.filter(role=0, status=0).values('school', 'app_date').order_by("id").reverse()
                
            for schl in schls:
                scl_obj = School.objects.get(pk=schl["school"])
                result = {'id': scl_obj.id, 'logo': scl_obj.logo, 'name': scl_obj.name,
                          'city': scl_obj.city, 'app_date': schl["app_date"]}
                data.append(result)
            

            paginator = PageNumberPagination()
            paginator.page_size = 10
            result_page = paginator.paginate_queryset(data, request)

            serializer = ser_schl_apps(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            return Response({'status': 0})
    else:
        return Response({"is_logged_in": 0})


@api_view(['POST'])
def show_specific_school(request):
    user = get_user_from_session(request.data["sessionid"])
    if user is not None:
        if user.user_info.role in [4,5]:
            data = {}
            scl = School.objects.get(pk=request.data["id"])

            data["user_name"] = scl.school_admins.user.first_name
            data["mbl_num"] = scl.school_admins.user.user_info.mbl_num
            data["landline"] = scl.school_admins.landline
            data["designation"] = scl.school_admins.designation
            data["name"] = scl.name
            data["email"] = scl.email
            data["province"] = scl.province
            data["city"] = scl.city
            data["tehsil"] = scl.tehsil
            data["web"] = scl.web
            data["type"] = scl.type
            data["play_area"] = scl.play_area
            data["status_of_property"] = scl.status_of_property
            data["area"] = scl.area
            data["total_stu"] = scl.total_stu
            data["logo"] = scl.logo
            data["location"] = scl.location
            data["address"] = scl.address
            data["max_teachers"] = scl.max_teachers
            classes = scl.classes_set.all()
            cl = []

            for b in classes:
                a = {"name": b.name, "max_stu": b.max_stu, "fee": b.fee}
                cl.append(a)
            data["classes"] = cl

            scl_imgs = scl.scl_images_set.all()
            count = 1
            for b in scl_imgs:
                data[f"pic{count}"] = b.pic
                count += 1
            school_data = ser_show_schl(data)

            return Response({'status': school_data.data})
        else:
            return Response({'status': 0})
    else:
        return Response({"is_logged_in": 0})


@api_view(['POST'])
def make_schedule(request):
    user = get_user_from_session(request.data["sessionid"])
    if user is not None:
        if user.user_info.role in [4,5]:
            try:
                data = request.data["date"]
                schl = request.data["schl_id"]
                schl = School.objects.get(pk=schl)
                data = data.split("T")
                date = list(map(int, data[0].split("-")))
                date_to_send = date.copy()
                time = list(map(int, data[1].split(":")))
                time_to_send = time.copy()
                date = datetime(date[0], date[1], date[2],
                                time[0], time[1], tzinfo=pytz.UTC)
                Schedule.objects.update_or_create(school=schl, defaults={'schedule': date})
                date_to_send = f"{date_to_send[2]}-{MONTHS[date_to_send[1]-1]}-{date_to_send[0]}"
                am = "AM"
                if time_to_send[0] > 12:
                    am = "PM"
                    time_to_send[0] -= 12
                time_to_send = f"{time_to_send[0]}:{time_to_send[1]} {am}"

                html_message = render_to_string(
                    'registration/schedule.html', {'date': date_to_send, 'time': time_to_send})
                plain_message = strip_tags(html_message)
                from_email = "From <info.itotpk@gmail.com>"
                to_email = schl.school_admins.user.email
                send_mail("ITOT Visiting Schedule...", plain_message,
                        from_email, [to_email], html_message=html_message)
                return Response({"status": 1})
            except:
                return Response({"status": 2})
        else:
            return Response({'status': 0})
    else:
        return Response({"is_logged_in": 0})


@api_view(['POST'])
def approve_school(request):
    user = get_user_from_session(request.data["sessionid"])
    if user is not None:
        if user.user_info.role in [4,5]:
            schl = School.objects.get(pk=request.data["schl_id"])
            l_k = schl.l_key
            schl.is_active = True
            schl.app_date = datetime.now()
            schl.save()
            Applications.objects.filter(school=schl, role=0).update(status=1)
            user__info = schl.school_admins.user.user_info
            user__info.role = 3
            user__info.save()
            try:
                schl.schedule.delete()
            except:
                pass

            html_message = render_to_string(
                'registration/app_school.html', {'l_k': l_k})
            plain_message = strip_tags(html_message)
            from_email = "From <info.itotpk@gmail.com>"
            to_email = schl.school_admins.user.email
            send_mail("School Registration Status...", plain_message,
                      from_email, [to_email], html_message=html_message)
            return Response({'status': 1})
        else:
            return Response({'status': 0})                   #not a super user
    else:
        return Response({"is_logged_in": 0})


@api_view(['POST'])
def reject_school(request):
    user = get_user_from_session(request.data["sessionid"])
    if user is not None:
        if user.user_info.role in [4,5]:
            reason = request.data["reason"]
            schl_id = request.data["schl_id"]
            schl = School.objects.get(pk=schl_id)
            schl.delete()
            html_message = render_to_string(
                'registration/rej_school.html', {'reason': reason})
            plain_message = strip_tags(html_message)
            from_email = "From <info.itotpk@gmail.com>"
            to_email = schl.school_admins.user.email
            send_mail("School Registration Status...", plain_message, from_email, [to_email], html_message=html_message)
            return Response({'status': 1})
        else:
            return Response({'status': 0})
    else:
        return Response({"is_logged_in": 0})


#************************* Schedules *******************************


@api_view(['POST'])
def today_schedules(request):
    user = get_user_from_session(request.data["sessionid"])
    if user is not None:
        if user.is_superuser:
            data_to_send = []
            data = Schedule.objects.all()
            for a in data:
                b = {}
                b["date"] = a.schedule
                b["logo"] = str(a.school.logo)
                if len(b["logo"]) != 0:
                    b["logo"] = "/media/"+b["logo"]
                b["id"] = a.school.id
                b["name"] = a.school.name
                b["address"] = a.school.address
                data_to_send.append(b)

            data = ser_schedules(data=data_to_send, many=True)
            if data.is_valid():
                return Response({'status': data.data})
            else:
                return Response({'status': 0})
        else:
            return Response({'admin': 0})
    else:
        return Response({"is_logged_in": 0})


@api_view(['POST'])
def all_schedules(request):
    user = get_user_from_session(request.data["sessionid"])
    if user is not None:
        if user.is_superuser:
            data_to_send = []
            data = Schedule.objects.all()
            for a in data:
                b = {}
                b["date"] = a.schedule
                b["logo"] = str(a.school.logo)
                if len(b["logo"]) != 0:
                    b["logo"] = "/media/"+b["logo"]
                b["id"] = a.school.id
                b["name"] = a.school.name
                b["address"] = a.school.address
                data_to_send.append(b)

            data = ser_schedules(data=data_to_send, many=True)
            if data.is_valid():
                return Response({'status': data.data})
            else:
                return Response({'status': 0})
        else:
            return Response({'admin': 0})
    else:
        return Response({"is_logged_in": 0})


@api_view(['POST'])
def passed_schedules(request):
    user = get_user_from_session(request.data["sessionid"])
    if user is not None:
        if user.is_superuser:
            data_to_send = []
            data = Schedule.objects.all()
            for a in data:
                b = {}
                b["date"] = a.schedule
                b["logo"] = str(a.school.logo)
                if len(b["logo"]) != 0:
                    b["logo"] = "/media/"+b["logo"]
                b["id"] = a.school.id
                b["name"] = a.school.name
                b["address"] = a.school.address
                data_to_send.append(b)

            data = ser_schedules(data=data_to_send, many=True)
            if data.is_valid():
                return Response({'status': data.data})
            else:
                return Response({'status': 0})
        else:
            return Response({'admin': 0})
    else:
        return Response({"is_logged_in": 0})


@api_view(['POST'])
def schedules_range(request):
    user = get_user_from_session(request.data["sessionid"])
    if user is not None:
        if user.is_superuser:
            in_date = request.data["in_date"]
            out_date = request.data["out_date"]
            data_to_send = []
            data = Schedule.objects.filter(schedule__range=(in_date, out_date))
            for a in data:
                b = {}
                b["date"] = a.schedule
                b["logo"] = str(a.school.logo)
                if len(b["logo"]) != 0:
                    b["logo"] = "/media/"+b["logo"]
                b["id"] = a.school.id
                b["name"] = a.school.name
                b["address"] = a.school.address
                data_to_send.append(b)

            data = ser_schedules(data=data_to_send, many=True)
            if data.is_valid():
                return Response({'data': data.data})
            else:
                return Response({'data': 0})
        else:
            return Response({'admin': 0})
    else:
        return Response({"is_logged_in": 0})
