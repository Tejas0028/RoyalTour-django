from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *

class Seeker_SignUp_Form(UserCreationForm):
    password1 = forms.CharField(required=True,label="Password",widget=forms.PasswordInput(attrs={'class':"mb-0 form-control",
                'placeholder':'Enter Password'}))
    password2 = forms.CharField(required=True,label="Confirm Password",widget=forms.PasswordInput(attrs={'class':"mb-0 form-control",'placeholder':'Enter Password Again'}))
    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={
                        'class':"mb-0 form-control",
                       'placeholder':'Enter Your Email'
                    }))
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        widgets = {
            'username' : forms.TextInput(attrs={
                'class':"mb-0 form-control",
                'placeholder':'Enter Your Username'
            }),
        }


class Seeker_Verify_Email_Form(forms.Form):
    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={
        'placeholder' : "Enter your Email",
        'class' : "form-control"
    }))


class Seeker_ForgotPassword_Form(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control','placeholder' : "Enter your Email"}))
    class Meta:
        model = User
        fields = ['email']


class Seeker_OtpVerify_Form(forms.Form):
     otp = forms.CharField(required=True, error_messages={'required':'Please enter OTP'} ,max_length=6, widget=forms.TextInput(
        attrs={'class': 'form-control','placeholder' : "Enter OTP",}))


class Seeker_Login_Form(AuthenticationForm):
    username = forms.CharField(required=True,label="Username",widget=forms.TextInput(attrs={'class':"form-control",'placeholder' : "Enter your Username",}))
    password = forms.CharField(required=True,label="Password",widget=forms.PasswordInput(attrs={'class':"form-control",'placeholder' : "Enter your Password"}))
    class Meta:
        model = User
        Fields = ['username','password']


class Seeker_UserForm(forms.ModelForm):
    username = forms.CharField(max_length=50,disabled=True,widget=forms.TextInput(
        attrs={
            'class' : 'form-control',
            'placeholder' : "Enter your Username",
        }
    ))
    email = forms.EmailField(max_length=50,disabled=True,widget=forms.EmailInput(
        attrs={
            'class' : 'form-control',
            'placeholder' : "Enter your Email",
        }
    ))
    class Meta:
        model = User
        fields = ['username','email']


class Seeker_ProfileForm(forms.ModelForm):
    class Meta:
        model = Seeker_Profile_Model
        fields =  ['avatar', 'fname', 'lname', 'tel', 'gender', 'age', 'address', 'area']

        widgets = {
            'avatar': forms.FileInput(attrs={
                'class':'form-control',
                'placeholder' : "Enter your Username",
            }),
            'fname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder':'First Name'
            }),
            'lname': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Last Name'
            }),
            'area': forms.Select(attrs={
                'class':'wide form-control',
                'placeholder':'Area'
            }),
            'gender' : forms.Select(attrs={
                'class':'wide form-control',
            }),
            'age' : forms.NumberInput(attrs={
                'class':'form-control',
                'placeholder' : "Enter your Age",
            }),
            'tel' : forms.NumberInput(attrs={
                'class':'form-control',
                'placeholder':'Phone Number',
            }),
            'address' : forms.Textarea(attrs={
                'class':'form-control',
                'placeholder':'Address',
                'rows': 4, 'cols': 60
            }),
        }
        labels = {
            'avatar': 'Profile picture',
            'fname': 'First name',
            'lname': 'Last name',
            'tel': 'Phone number',
            'gender': 'Gender',
            'age': 'Age',
            'address': 'Address',
            'area': 'City'
        }

class TripQuotationForm(forms.ModelForm):
    departure_date = forms.DateField(
        label='Departure Date',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    number_of_adults = forms.IntegerField(
        label='Number of Adults',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Number of Adults'})
    )
    number_of_children = forms.IntegerField(
        label='Number of Children',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Number of Children'})
    )
    notes = forms.CharField(
        label='Additional Notes',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Additional notes'})
    )

    class Meta:
        model = TripQuotation
        fields = ['departure_date', 'number_of_adults', 'number_of_children', 'notes']
        labels = {
            'departure_date': 'Departure Date',
            'number_of_adults': 'Number of Adults',
            'number_of_children': 'Number of Children',
            'notes': 'Additional Notes'
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'email', 'subject', 'message')
    
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'placeholder': self.fields[field].label,
            })
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('.com'):
            raise forms.ValidationError('Please enter a valid email address.')
        return email
