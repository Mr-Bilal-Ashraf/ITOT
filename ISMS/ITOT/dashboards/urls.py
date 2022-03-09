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


    #********* School ************


    #********* Teachers ***********

    path('staff/sample/teachers/', staff_views.sample_teachers, name="sample_teachers"),
    path('staff/all/teachers/', staff_views.all_teachers, name="all_teachers"),
    path('staff/filter/teachers/', staff_views.school_filtered_teachers, name="filtered_teachers"),




    #********* Students ***********

    path('staff/sample/students/', staff_views.sample_students, name="sample_students"),
    path('staff/all/students/', staff_views.all_students, name="all_students"),
    path('staff/filter/students/', staff_views.school_filtered_students, name="filtered_students"),




    # path('staff/', staff_views., name="a"),
#********************* School Dashboard ************************ 



    # path('school/', school_views., name="b"),
#********************* Teacher Dashboard ***********************



    # path('teacher/', teacher_views., name="c"),
#********************* Student Dashboard ***********************



    # path('student/', student_views., name="d"),
]
