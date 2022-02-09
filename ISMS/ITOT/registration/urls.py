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
    # path('forgot/password/reset/', views.forgot_password_reset, name="forgot_password_reset"),
    


    path('del/', views.del_user, name="del_user"),

]
