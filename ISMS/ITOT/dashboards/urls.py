from django.urls import path
from . import staff_views, school_views, teacher_views, student_views

urlpatterns = [

#********************* Staff Dashboard *************************

    #********* School **************
    # path('staff/school/', staff_views., name="a"),



    #********* Applications *********

    path('staff/show/apps/', staff_views.show_school_applications, name="show_school_applications"),
    path('staff/show/details/', staff_views.show_specific_school, name="show_specific_school"),
    path('staff/schedule/make/', staff_views.make_schedule, name="make_schedule"),
    path('staff/app/', staff_views.approve_school, name="approve_school"),
    path('staff/rej/', staff_views.reject_school, name="reject_school"),

    #********* Schedules *********

    path('staff/schedule/today/', staff_views.today_schedules, name="today_schedules"),
    path('staff/schedule/all/', staff_views.all_schedules, name="all_schedules"),
    path('staff/schedule/passed/', staff_views.passed_schedules, name="passed_schedules"),
    path('staff/schedule/range/', staff_views.schedules_range, name="schedules_range"),

    #********* Teachers ***********

    path('staff/teacher/sample/', staff_views.sample_teachers, name="sample_teachers"),
    path('staff/teacher/all/', staff_views.all_teachers, name="all_teachers"),
    path('staff/teacher/filter/', staff_views.school_filtered_teachers, name="filtered_teachers"),
    path('staff/teacher/detail/', staff_views.teacher_detail, name="teacher_detail"),

    #********* Students ***********

    path('staff/student/sample/', staff_views.sample_students, name="sample_students"),
    path('staff/student/all/', staff_views.all_students, name="all_students"),
    path('staff/student/filter/', staff_views.school_filtered_students, name="filtered_students"),
    path('staff/student/detail/', staff_views.student_detail, name="student_detail"),

    #********* Dashboard ***********

    path('staff/counts/', staff_views.dashboard_counts, name="dashboard_counts"),



#********************* School Dashboard ************************ 



    # path('school/', school_views., name="b"),
#********************* Teacher Dashboard ***********************



    # path('teacher/', teacher_views., name="c"),
#********************* Student Dashboard ***********************



    # path('student/', student_views., name="d"),
]
