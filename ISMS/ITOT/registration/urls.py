from django.urls import path
from . import views

urlpatterns = [

    path('sign/up/', views.sign_up, name="create_user"),
    path('sign/in/', views.sign_in, name="log_in"),
    path('sign/out/', views.sign_out, name="Log_Out"),
    path('<int:id>/conf/code/<str:code>/', views.confirm_code, name="confirm_code"),                        #link in email to verify account
    path('forgot/password/', views.forgot_password, name="forgot_password"),                                #get email OR username and send reset password email
    path('forgot/password/reset/', views.forgot_password_reset, name="forgot_password_reset"),              #get code and new password to reset password
    path('update/password/', views.update_password, name="update_password"),                                #update password from settings, get old & new password
    path('profile/update/', views.update_profile, name="update_profile"),                                   #will update profile data like image and name etc
    path('is/complete/', views.is_complete, name="is_complete"),                                            #check is the user has setup his profile or not 
    path('school/', views.register_school, name="register_school"),
    path('update/logo/', views.update_logo, name="update_logo"),
    path('profile/get/', views.get_profile, name="get_profile"),
    path('rej/school/', views.reject_school, name="reject_school"),
    path('app/school/', views.approve_school, name="approve_school"),
    path('show/school/apps/', views.show_school_applications, name="show_school_applications"),
    # path('forgot/password/reset/', views.forgot_password_reset, name="forgot_password_reset"),





    path('check/', views.check, name="check"),
    path('del/', views.del_user, name="del_user"),

]
