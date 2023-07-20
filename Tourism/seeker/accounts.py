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


def Seeker_Reg(request):
    if request.session.get('seeker') != None:
        return redirect('Seeker:seeker_profile')
    if request.method == "POST":
        seeker_registration = Seeker_SignUp_Form(request.POST)
        if seeker_registration.is_valid():
            if User.objects.filter(email__iexact = seeker_registration.cleaned_data['email']):
                # if User.objects.filter(email__iexact=ucf.cleaned_data['email']):
                messages.error(request,"Email is already registered...")
            else:
                seeker_registration.save()
                reg = seeker_names(user=User.objects.get(username=seeker_registration.cleaned_data['username']))
                reg.save()
                seeker_update = User.objects.get(username = seeker_registration.cleaned_data['username'])
                seeker_update.is_active = False
                seeker_update.save()
                request.session['seeker_name'] = seeker_registration.cleaned_data['username']
                request.session['seeker_email'] = seeker_registration.cleaned_data['email']
                subject = 'Verification Mail'
                message = f'Hello {seeker_update.username},' + "\nEmail : " + seeker_update.email + \
                    "\nPlease verify your email id.. http://127.0.0.1:8000/seeker_verify/"
                email_from = settings.EMAIL_HOST_USER
                email_to = [seeker_update.email, ]
                send_mail(subject, message, email_from, email_to)
                return redirect('Seeker:seeker_verify_email_sent')
        else:
            messages.error(request,"Something went wrong")
            redirect('Seeker:seeker_reg')
    else:
        seeker_registration = Seeker_SignUp_Form()
    template = "Seeker/seeker_reg.html"
    return render(request,template,{'seeker_form':seeker_registration})


def Seeker_Verify_Email(request):
    if request.session.get('seeker') != None:
        request.session.delete()
        return redirect('Seeker:seeker_profile')

    if request.method == "POST":
        seeker_verify_email = Seeker_Verify_Email_Form(request.POST)
        if seeker_verify_email.is_valid():
            email = seeker_verify_email.cleaned_data['email']
            if not User.objects.filter(email__iexact = email):
                messages.error(request,'Email and seeker not found, please signup!')
                return redirect('Seeker:seeker_reg')
            seeker_email = User.objects.get(email__iexact = email)
            if (seeker_email.is_active == True):
                messages.error(request,f'{seeker_email.email} is already activated')
                messages.error(request,'Please Login')
                return redirect('Seeker:seeker_login')
            else:
                seeker_email.is_active = True
                seeker_email.is_staff = False
                seeker_email.save()
                seeker = {
                    'username' : seeker_email.username,
                    'seeker_email': seeker_email.email
                }
                request.session['seeker'] = seeker
    else:
        seeker_verify_email = Seeker_Verify_Email_Form()
    return render(request,'Seeker/seeker_verify_mail.html',{'seeker_form_verify':seeker_verify_email })


def Seeker_Sent_Mail(request):
    return render(request,'Seeker/seeker_verification_sent.html')


def Seeker_Login(request):
    if (request.session.get('seeker') != None):
        return redirect('Seeker:seeker_profile')
    if request.method == "POST":
        seeker_login = Seeker_Login_Form(request = request,data = request.POST)
        if seeker_login.is_valid():
            seeker = authenticate(
                username = seeker_login.cleaned_data['username'],
                password = seeker_login.cleaned_data['password'],
            )
            if seeker != None:
                seeker_data = User.objects.get(username = seeker)
                if seeker_data.is_active == True and seeker_data.is_staff == False:
                    seeker = {
                        'username' : seeker_data.username,
                        'seeker_email' : seeker_data.email
                    }
                    request.session['seeker'] = seeker
                    request.session['seeker_email'] = seeker_data.email
                    return redirect('Seeker:seeker_profile')
                else:
                    messages.error(request,"User not found")
                    return redirect('Seeker:seeker_reg')
            else:
                messages.error(request,"Seeker not Found...")
                return redirect('Seeker:seeker_reg')
        else:
            messages.error(request,"Pleaser Enter Valid Username or Password")
            return redirect('Seeker:seeker_login')
    else:
        login = Seeker_Login_Form()
    tdonerlate = "Seeker/seeker_login.html"
    return render(request,tdonerlate,{'login_form' : login})

def Seeker_Profile(request):
    if request.session.get('seeker') != None:
        epl = request.session.get('seeker')
        if not User.objects.filter(username__iexact=epl['username']).exists():
            messages.error(request,"User not found")
            request.session.delete()
            return redirect('Seeker:seeker_login')
        user = User.objects.get(username=epl['username'])
        if request.method == "POST":
            seeker_user_form = Seeker_UserForm(request.POST or None, instance=user)
            seeker_profile_form = Seeker_ProfileForm(
                request.POST or None, request.FILES or None, instance=user.seeker_names.seeker_profile_model)
            if seeker_user_form.is_valid() and seeker_profile_form.is_valid():
                seeker_user_form.save()
                seeker_profile_form.save()
                messages.success(request, 'Account Details Saved Successfully')
                return redirect('Seeker:seeker_profile')
            else:
                messages.error(request, 'Please correct the error below')
        else:
            seeker_user_form = Seeker_UserForm(instance=user)
            seeker_profile_form = Seeker_ProfileForm(instance=user.seeker_names.seeker_profile_model)
        seeker_profile_user = Seeker_Profile_Model.objects.get(user=user.seeker_names.seeker_profile_model)
        if seeker_profile_user.avatar is None:
            seeker_image = None
        else:
            seeker_image = seeker_profile_user
        return render(request,"Seeker/seeker_profile.html", {'seeker_user_form': seeker_user_form, 'seeker_profile_form': seeker_profile_form,
        'img' : seeker_image.avatar.url})
    else:
        return redirect('Seeker:seeker_login')


def Seeker_ForgotPassword(request):
    if request.method == "POST":
        fp = Seeker_ForgotPassword_Form(request.POST)
        if fp.is_valid():
            email = request.POST.get('email')
            is_email = User.objects.filter(email__iexact=email).exists()
            if is_email:
                OTP = random.randint(111111,999999)
                subject = 'Password Reset OTP'
                message = "Your OTP is, " + \
                    str(OTP) + "\nPlease Follow This Link to verify OTP, --> http://http://127.0.0.1:8000/seeker_otpverify/"
                email_from = settings.EMAIL_HOST_USER
                email_to = [email, ]
                send_mail(subject, message, email_from, email_to)

                request.session["reset_password_OTP"] = OTP
                request.session["reset_password_EMAIL"] = email
                request.session.set_expiry(900)
                return redirect('Seeker:seeker_otpverify')
            else:
               messages.error(request,"Email not found, please signup!") 
               return redirect('Seeker:seeker_reg')
        else:
            messages.error(request,"Form is invalid")
    else:
        fp = Seeker_ForgotPassword_Form()
    tdonerlate = "Seeker/seeker_forgot_password.html"
    return render(request,tdonerlate,{'form':fp})


def Seeker_OtpVerify(request):
    if request.method == 'POST':
        omf = Seeker_OtpVerify_Form(request.POST)
        otp = request.POST.get('otp')
        session_otp = request.session.get('reset_password_OTP')
        if str(otp) == str(session_otp):
            return redirect('Seeker:seeker_resetpw')
        else:
            messages.error(request,"Please enter valid OTP")
            return redirect('Seeker:seeker_otpverify')
    else:
        omf = Seeker_OtpVerify_Form()
    tdonerlate = "Seeker/seeker_otp_verification.html"
    return render(request, tdonerlate, {'form':omf})


def Seeker_ResetPassword(request):
    if request.method == "POST":
        password = request.POST['password1']
        c_password = request.POST['password2']
        if password == c_password:
            email_var = request.session.get('reset_password_EMAIL')
            usr = User.objects.get(email=email_var)
            usr.set_password(password)
            usr.save()
            request.session.delete()
            return redirect('Seeker:seeker_login')
    tdonerlate = "Seeker/seeker_reset_password.html"
    return render(request,tdonerlate)


def Seeker_Logout(request):
    if (request.session.get('seeker') != None):
        logout(request)
        return redirect('Seeker:seeker_login')
    else:
        return redirect('Seeker:seeker_login')

def Seeker_set_password(request):
    if request.session.get('seeker') == None:
        return redirect('Seeker:seeker_login')
    user_data = request.session.get('seeker')
    if request.method == "POST":
        old = request.POST.get('old_password')
        pass1 = request.POST.get('new_password1')
        pass2 = request.POST.get('new_password2')
        user = User.objects.get(email__iexact = request.session.get('seeker_email'))
        if pass1 == pass2:
            if check_password(old, user.password):
                user.set_password(pass1)
                user.save()
                messages.success(request,"Password has been updated successfully!")
                return redirect("Seeker:seeker_profile")
            else:
                messages.error(request,"old password is wrong")
                return redirect("Seeker:Seeker_set_password")
        else:
            messages.error(request,"New and Confirm password not same")
            return redirect("Seeker:Seeker_set_password")
    template = "Seeker/seeker_set_password.html"
    return render(request,template,{'name':user_data})