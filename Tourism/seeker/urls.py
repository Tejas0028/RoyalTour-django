from django.urls import *
from .views import *

app_name = "Seeker"

urlpatterns = [
    path('',index,name="index"),
    path('seeker_reg/',Seeker_Reg, name = "seeker_reg"),
    path('seeker_verify/',Seeker_Verify_Email, name = "seeker_verify_mail"),
    path('seeker_verify_mail/',Seeker_Sent_Mail, name = "seeker_verify_email_sent"),
    path('seeker_login/',Seeker_Login, name = "seeker_login"),
    path('seeker_profile/',Seeker_Profile, name = "seeker_profile"),
    path('seeker_forgotpassword',Seeker_ForgotPassword,name="seeker_forgotpw"),
    path('seeker_otpverify/',Seeker_OtpVerify,name="seeker_otpverify"),
    path('seeker_resetpw/',Seeker_ResetPassword,name="seeker_resetpw"),
    path('Seeker_set_password/',Seeker_set_password,name="Seeker_set_password"),
    path('seeker_logout/',Seeker_Logout, name = 'seeker_logout'),
    path('seeker_destination_detail/<int:destination_id>/',seeker_destination_detail,name="seeker_destination_detail"),
    path('trip_quotation/<int:destination_id>/',trip_quotation,name="trip_quotation"),
    path('requested_quotes/',requested_quotes,name="requested_quotes"),
    path('search/', search_destinations, name='search_destinations'),
    path('search_cat/<int:category_id>/',search_cat,name="search_cat"),
    path('requested_quotes_data/<int:id>/',requested_quotes_data,name="requested_quotes_data"),
    path('contact/',contact,name="contact"),
    path('aboutus/',aboutus,name='aboutus'),

]
