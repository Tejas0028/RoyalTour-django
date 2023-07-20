from django.urls import *
from .views import *

app_name = "Provider"

urlpatterns = [
    path('',Provider_Reg, name = "provider_reg"),
    path('provider_verify/',Provider_Verify_Email, name = "provider_verify_mail"),
    path('provider_verify_mail/',Provider_Sent_Mail, name = "provider_verify_email_sent"),
    path('provider_login/',Provider_Login, name = "provider_login"),
    path('provider_profile/',Provider_Profile, name = "provider_profile"),
    path('provider_forgotpassword',Provider_ForgotPassword,name="provider_forgotpw"),
    path('provider_otpverify/',Provider_OtpVerify,name="provider_otpverify"),
    path('provider_resetpw',Provider_ResetPassword,name="provider_resetpw"),
    path('provider_logout/',Provider_Logout, name = 'provider_logout'),
    path('provider_set_password/',Provider_set_password,name="provider_set_password"),
    path('destination_quotes/',destination_quotes,name="destination_quotes"),
    path('provide_quote/<int:trip_quotation_id>/',provide_quote,name="provide_quote"),
    path('reports/',MyReport,name="MyReport"),
    path('service_report/',MyServiceReport,name="MyServiceReport"),
    path('trip-quotation/<int:trip_quotation_id>/add-hotel-data/', add_hotel_data, name='add_hotel_data'),

]