from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
from .forms import *
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, logout
from seeker.models import *
import random
from django.contrib.auth.hashers import check_password


def Provider_Reg(request):
    if request.session.get('provider') != None:
        return redirect('Provider:provider_profile')
    if request.method == "POST":
        provider_registration = Provider_SignUp_Form(request.POST)
        if provider_registration.is_valid():
            if User.objects.filter(email__iexact = provider_registration.cleaned_data['email']):
                # if User.objects.filter(email__iexact=ucf.cleaned_data['email']):
                messages.error(request,"Email is already registered...")
            else:
                provider_registration.save()
                reg = provider_names(user=User.objects.get(username=provider_registration.cleaned_data['username']))
                reg.save()
                provider_update = User.objects.get(username = provider_registration.cleaned_data['username'])
                provider_update.is_active = False
                provider_update.save()
                request.session['provider_name'] = provider_registration.cleaned_data['username']
                request.session['provider_email'] = provider_registration.cleaned_data['email']

                       #sending verfication mail

                subject = 'Verification Mail'
                message = f'Hello {provider_update.username},' + "\nEmail : " + provider_update.email + \
                    "\nPlease verify your email id.. http://127.0.0.1:8000/provider/provider_verify/"
                email_from = settings.EMAIL_HOST_USER
                email_to = [provider_update.email, ]
                send_mail(subject, message, email_from, email_to)
                return redirect('Provider:provider_verify_email_sent')
        else:
            messages.error(request,"Something went wrong")
            redirect('Provider:provider_reg')
    else:
        provider_registration = Provider_SignUp_Form()
    template = "Provider/provider_reg.html"
    return render(request,template,{'provider_form':provider_registration})


def Provider_Verify_Email(request):
    if request.session.get('provider') != None:
        request.session.delete()
        return redirect('Provider:provider_profile')

    if request.method == "POST":
        provider_verify_email = Provider_Verify_Email_Form(request.POST)
        if provider_verify_email.is_valid():
            email = provider_verify_email.cleaned_data['email']
            if not User.objects.filter(email__iexact = email):
                messages.error(request,'Email and provider not found, please signup!')
                return redirect('Provider:provider_reg')
            provider_email = User.objects.get(email__iexact = email)
            if (provider_email.is_active == True):
                messages.error(request,f'{provider_email.email} is already activated')
                messages.error(request,'Please Login')
                return redirect('Provider:provider_login')
            else:
                provider_email.is_active = True
                provider_email.is_staff = True
                provider_email.save()
                provider = {
                    'username' : provider_email.username,
                    'provider_email': provider_email.email
                }
                request.session['provider'] = provider
    else:
        provider_verify_email = Provider_Verify_Email_Form()
    return render(request,'Provider/provider_verify_mail.html',{'provider_form_verify':provider_verify_email })


def Provider_Sent_Mail(request):
    return render(request,'Provider/provider_verification_sent.html')


def Provider_Login(request):
    if request.session.get('provider') != None:
        return redirect('Provider:provider_profile')
    if request.method == "POST":
        provider_login = Provider_Login_Form(request = request,data = request.POST)
        if provider_login.is_valid():
            provider = authenticate(
                username = provider_login.cleaned_data['username'],
                password = provider_login.cleaned_data['password'],
            )
            if provider != None:
                provider_data = User.objects.get(username = provider)
                if provider_data.is_active == True and provider_data.is_staff == True:
                    provider = {
                        'username' : provider_data.username,
                        'provider_email' : provider_data.email
                    }
                    request.session['provider'] = provider
                    request.session['provider_email'] = provider_data.email
                    return redirect('Provider:provider_profile')
                else:
                    messages.error(request,"User not found!")
                    return redirect('Provider:provider_reg')
            else:
                messages.error(request,"Provider not Found...")
                return redirect('Provider:provider_reg')
        else:
            messages.error(request,"Pleaser Enter Valid Username or Password")
            return redirect('Provider:provider_login')
    else:
        login = Provider_Login_Form()
    tproviderlate = "Provider/provider_login.html"
    return render(request,tproviderlate,{'login_form' : login})


def Provider_Profile(request):
    if request.session.get('provider') != None:
        epl = request.session.get('provider')
        if not User.objects.filter(username__iexact=epl['username']).exists():
            messages.error(request,"User not found")
            request.session.delete()
            return redirect('Provider:provider_login')
        user = User.objects.get(username=epl['username'])
        if request.method == "POST":
            provider_user_form = Provider_UserForm(request.POST or None, instance=user)
            provider_profile_form = Provider_ProfileForm(
                request.POST or None, request.FILES or None, instance=user.provider_names.provider_profile_model)
            if provider_user_form.is_valid() and provider_profile_form.is_valid():
                provider_user_form.save()
                provider_profile_form.save()
                messages.success(request, 'Account Details Saved Successfully')
                return redirect('Provider:provider_profile')
            else:
                messages.error(request, 'Please correct the error below')
        else:
            provider_user_form = Provider_UserForm(instance=user)
            provider_profile_form = Provider_ProfileForm(instance=user.provider_names.provider_profile_model)
        provider_profile_user = Provider_Profile_Model.objects.get(user=user.provider_names.provider_profile_model)
        if provider_profile_user.avatar is None:
            provider_image = None
        else:
            provider_image = provider_profile_user
        return render(request,"Provider/provider_profile.html", {'provider_user_form': provider_user_form, 'provider_profile_form': provider_profile_form,
        'img' : provider_image.avatar.url})
    else:
        return redirect('Provider:provider_login')


def Provider_ForgotPassword(request):
    if request.method == "POST":
        fp = Provider_ForgotPassword_Form(request.POST)
        if fp.is_valid():
            email = request.POST.get('email')
            is_email = User.objects.filter(email__iexact=email).exists()
            if is_email:
                OTP = random.randint(111111,999999)
                subject = 'Password Reset OTP'
                message = "Your OTP is, " + \
                    str(OTP) + "\nPlease Follow This Link to verify OTP, --> http://http://127.0.0.1:8000/provider/provider_otpverify/"
                email_from = settings.EMAIL_HOST_USER
                email_to = [email, ]
                send_mail(subject, message, email_from, email_to)

                request.session["reset_password_OTP"] = OTP
                request.session["reset_password_EMAIL"] = email
                request.session.set_expiry(900)
                return redirect('Provider:provider_otpverify')
            else:
               messages.error(request,"Email not found, please signup!") 
               return redirect('Provider:provider_reg')
        else:
            messages.error(request,"Form is invalid")
    else:
        fp = Provider_ForgotPassword_Form()
    tproviderlate = "Provider/provider_forgot_password.html"
    return render(request,tproviderlate,{'form':fp})


def Provider_OtpVerify(request):
    if request.method == 'POST':
        omf = Provider_OtpVerify_Form(request.POST)
        otp = request.POST.get('otp')
        session_otp = request.session.get('reset_password_OTP')
        if str(otp) == str(session_otp):
            return redirect('Provider:provider_resetpw')
        else:
            messages.error(request,"Please enter valid OTP")
            return redirect('Provider:provider_otpverify')
    else:
        omf = Provider_OtpVerify_Form()
    tproviderlate = "Provider/provider_otp_verification.html"
    return render(request, tproviderlate, {'form':omf})


def Provider_ResetPassword(request):
    if request.method == "POST":
        password = request.POST['password1']
        c_password = request.POST['password2']
        if password == c_password:
            email_var = request.session.get('reset_password_EMAIL')
            usr = User.objects.get(email=email_var)
            usr.set_password(password)
            usr.save()
            request.session.delete()
            return redirect('Provider:provider_login')
    tproviderlate = "Provider/provider_reset_password.html"
    return render(request,tproviderlate)


def Provider_Logout(request):
    if (request.session.get('provider') != None):
        logout(request)
        return redirect('Provider:provider_login')
    else:
        return redirect('Provider:provider_login')

def Provider_set_password(request):
    if request.session.get('provider') == None:
        return redirect('Provider:provider_login')
    user_data = request.session.get('provider')
    if request.method == "POST":
        old = request.POST.get('old_password')
        pass1 = request.POST.get('new_password1')
        pass2 = request.POST.get('new_password2')
        user = User.objects.get(email__iexact = request.session.get('provider_email'))
        if pass1 == pass2:
            if check_password(old, user.password):
                user.set_password(pass1)
                user.save()
                messages.success(request,"Password has been updated successfully!")
                return redirect("Provider:provider_profile")
            else:
                messages.error(request,"old password is wrong")
                return redirect("Provider:provider_set_password")
        else:
            messages.error(request,"New and Confirm password not same")
            return redirect("Provider:provider_set_password")
    template = "Provider/provider_set_password.html"
    return render(request,template,{'name':user_data})