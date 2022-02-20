from django.urls import path
from . import views, school_views, user_views, teacher_views

urlpatterns = [


    # path('forgot/password/reset/', views.forgot_password_reset, name="forgot_password_reset"),


    path('check/', views.check, name="check"),
    path('del/', views.del_user, name="del_user"),


#********************* School APIs ************************ 

    path('range/schedules/', school_views.schedules_range, name="schedules_range"),
    path('rej/school/', school_views.reject_school, name="reject_school"),
    path('app/school/', school_views.approve_school, name="approve_school"),
    path('show/school/apps/', school_views.show_school_applications, name="show_school_applications"),
    path('show/school/details/', school_views.show_specific_school, name="show_specific_school"),
    path('school/list/', school_views.schl_list, name="show_school_list"),
    path('make/schedule/', school_views.make_schedule, name="make_schedule"),
    path('all/schedules/', school_views.all_schedules, name="all_schedules"),
    path('school/', school_views.register_school, name="register_school"),
    path('update/logo/', school_views.update_logo, name="update_logo"),


#********************* General User APIs *******************

    path('sign/up/', user_views.sign_up, name="create_user"),
    path('sign/in/', user_views.sign_in, name="log_in"),
    path('sign/out/', user_views.sign_out, name="Log_Out"),
    path('sign/out/all/', user_views.sign_out_all, name="Log_Out_ALL"),
    path('<int:id>/conf/code/<str:code>/', user_views.confirm_code, name="confirm_code"),                        #link in email to verify account
    path('forgot/password/', user_views.forgot_password, name="forgot_password"),                                #get email OR username and send reset password email
    path('forgot/password/reset/', user_views.forgot_password_reset, name="forgot_password_reset"),              #get code and new password to reset password
    path('update/password/', user_views.update_password, name="update_password"),                                #update password from settings, get old & new password
    path('profile/update/', user_views.update_profile, name="update_profile"),                                   #will update profile data like image and name etc
    path('is/complete/', user_views.is_complete, name="is_complete"),                                            #check is the user has setup his profile or not 
    path('profile/get/', user_views.get_profile, name="get_profile"),

#*********************** Teacher APIs ************************ 

    path('teacher/', teacher_views.register_teacher, name="register_teacher"),
    path('teachers/apps/', teacher_views.teachers_applications, name="teachers_applications"),
    path('my/classes/', teacher_views.my_classes, name="class_names_list"),
    path('rej/teacher/', teacher_views.reject_teacher_application, name="reject_teacher_application"),
    path('app/teacher/', teacher_views.approve_teacher_application, name="approve_teacher_application"),


    # path('forgot/password/reset/', teacher_views.forgot_password_reset, name="forgot_password_reset"),

]
