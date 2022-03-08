from django.urls import path
from . import staff_views, school_views, teacher_views, student_views

urlpatterns = [

#********************* Staff Dashboard *************************

    #********* Applications *********

    path('staff/show/apps/', staff_views.show_school_applications, name="show_school_applications"),
    path('staff/show/details/', staff_views.show_specific_school, name="show_specific_school"),
    path('staff/make/schedule/', staff_views.make_schedule, name="make_schedule"),
    path('staff/app/', staff_views.approve_school, name="approve_school"),
    path('staff/rej/', staff_views.reject_school, name="reject_school"),

    #********* Schedules *********

    path('staff/today/schedules/', staff_views.today_schedules, name="today_schedules"),
    path('staff/all/schedules/', staff_views.all_schedules, name="all_schedules"),
    path('staff/passed/schedules/', staff_views.passed_schedules, name="passed_schedules"),
    path('staff/range/schedules/', staff_views.schedules_range, name="schedules_range"),


    #********* School *********




    # path('staff/', staff_views., name="a"),
#********************* School Dashboard ************************ 



    # path('school/', school_views., name="b"),
#********************* Teacher Dashboard ***********************



    # path('teacher/', teacher_views., name="c"),
#********************* Student Dashboard ***********************



    # path('student/', student_views., name="d"),
]
