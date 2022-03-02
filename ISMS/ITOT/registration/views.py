from django.shortcuts import render
from django.contrib.sessions.models import Session
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from random import randint
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail


from .models import ConfCode


# *****************************************************************************************************************

MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
CLASSES = {'Pre Year 1': "P01",
           'Pre Year 2': "P02",
           'Pre Year 3': "P03",
           'Grade 1': "G01",
           'Grade 2': "G02",
           'Grade 3': "G03",
           'Grade 4': "G04",
           'Grade 5': "G05",
           'Grade 6': "G06",
           'Grade 7': "G07",
           'Grade 8': "G08",
           'Grade 9': "G09",
           'Grade 10': "G10"}


def get_user_from_session(id):
    try:
        session = Session.objects.get(session_key=id)
        session_data = session.get_decoded()
        uid = session_data.get('_auth_user_id')
        return User.objects.get(id=uid)
    except:
        return None


def email_reset_password(user):
    code = randint(111111, 999999)
    b = randint(11, 99)
    a = ConfCode.objects.update_or_create(
        user=user, defaults={"Con_code": code})
    html_message = render_to_string(
        'registration/for_pas_email.html', {"code": f"{code:06}#{b:02}#{user.id:03}"})
    plain_message = strip_tags(html_message)
    from_email = "From <mr.bilal2066@gmail.com>"
    to_email = user.email
    send_mail("Reset Your Password...", plain_message,
              from_email, [to_email], html_message=html_message)


def remove_all_sessions(id):
    user_sessions = []
    for session in Session.objects.all():
        if str(id) == session.get_decoded().get('_auth_user_id'):
            user_sessions.append(session.pk)
    return Session.objects.filter(pk__in=user_sessions).delete()


# ******************************************************************************************************************


@api_view(['GET'])
def check(request):
    print(request.COOKIES)
    res = render(request, 'registration/check.html')
    res.set_cookie("a","hy")
    return res


@api_view(['GET'])
def del_user(request):
    print(request.user)
    # User.objects.get(pk=7).delete()
    return Response({'a': 1})


# {"username":"Bilal","email":"mr.azaad622@gmail.com","password":"12345"}
