from datetime import datetime
import pytz
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from .views import get_user_from_session, MONTHS


from .models import Schedule, School, School_Admins, Classes, Applications, Scl_images
from .serializers import ser_logo, ser_schedules, ser_schl_apps, ser_srch_school, ser_reg_classes, ser_reg_school, ser_reg_admin, ser_show_schl, ser_det_schl


@api_view(['POST'])
def register_school(request):
    result = {"role": 0, "admin": 0, 'status': 0, "applications": 0}
    user = get_user_from_session(request.data["sessionid"])
    result["applications"] = len(
        Applications.objects.filter(user=user, role=1))
    if user is not None:
        # ROLE 0 => user, 1 => student, 2 => teacher, 3 => admin
        result["role"] = user.user_info.role
        # admin = 0 means user holds no school
        result["admin"] = 1 if School_Admins.objects.filter(user=user) else 0

        if result["admin"] == 0 and result["role"] == 0 and result["applications"] == 0:
            ser_school = ser_reg_school(data=request.data["school"])
            ser_admin = ser_reg_admin(data=request.data["admin"])
            ser_classes = ser_reg_classes(
                data=request.data["classes"], many=True)
            if ser_school.is_valid() and ser_classes.is_valid() and ser_admin.is_valid():
                schl = ser_school.save()

                schl_name = schl.name.upper().split(" ")
                schl_abbr = ""
                for a in schl_name:
                    schl_abbr += a[0]
                schl_abbr = schl_abbr[:3]

                city_name = schl.city.split("-")

                l_k = f"{schl_abbr}-{city_name[1]}-A{schl.id:02}"
                schl.l_key = l_k
                schl.save()

                ser_admin.create(user, schl)
                for a in ser_classes.data:
                    data = {}
                    for key, value in a.items():
                        data[key] = value
                    Classes.objects.create(
                        school=schl, name=data["name"], max_stu=data["max_stu"], fee=data["fee"])

                Applications.objects.create(
                    user=user, school=schl, role=0)
                Scl_images.objects.create(school=schl, text="pic1")
                Scl_images.objects.create(school=schl, text="pic2")
                Scl_images.objects.create(school=schl, text="pic3")

                result["status"] = 1
                return Response(result)
            else:
                # data not valid
                result["status"] = 0
                return Response(result)
        else:
            # status 0 operation fail for school application
            return Response(result)
    else:
        return Response({"is_logged_in": 0})


@api_view(['POST'])
def update_logo(request):
    user = get_user_from_session(request.data["sessionid"])
    if user is not None:
        request.data._mutable = True
        for x in request.data:
            if request.data[x] == "null":
                request.data[x] = None

        data = ser_logo(data=request.data)
        if data.is_valid():
            data.update(user)
            return Response({"status": 1})
        else:
            print(data.errors)
            return Response({"status": 0})
    else:
        return Response({"is_logged_in": 0})


@api_view(['POST'])
def schl_list(request):
    srch_query = {}
    try:
        for key, value in request.data.items():
            srch_query[key] = value.lower()
        srch_query["is_active"] = True
        resulted_schools = School.objects.filter(
            **srch_query).values("id", "logo", "name", "address")
        da = []
        for a in resulted_schools:
            d = {}
            for key, value in a.items():
                if key == "logo" and len(value) != 0:
                    value = "/media/"+value
                d[key] = value
            da.append(d)

        resulted_schools = ser_srch_school(data=da, many=True)
        if resulted_schools.is_valid():
            return Response({"schools": resulted_schools.data})
        return Response({"status": 0})
    except:
        return Response({"status": 0})


@api_view(['POST'])
def searched_school_detail(request):
    data = {}
    try:
        schl_id = request.data["schl_id"]
        scl = School.objects.get(pk=schl_id)
    except:
        # no school
        return Response({'status': 0})
    else:
        data["user_name"] = scl.school_admins.user.first_name
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
        data["address"] = scl.address

        scl_imgs = scl.scl_images_set.all()
        count = 1
        for b in scl_imgs:
            data[f"pic{count}"] = b.pic
            count += 1
        school_data = ser_det_schl(data)

        return Response({'schoolData': school_data.data})
