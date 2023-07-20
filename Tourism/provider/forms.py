from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .models import *
from seeker.models import Provide_TripQuotation,Add_hotel_data

class Provider_SignUp_Form(UserCreationForm):
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
                'placeholder':'Enter Your Username',
                'aria-label':"User Name"
            }),
        }


class Provider_Verify_Email_Form(forms.Form):
    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={
        'placeholder' : "Enter your Email",
        'class' : "form-control"
    }))


class Provider_ForgotPassword_Form(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control',}))
    class Meta:
        model = User
        fields = ['email']


class Provider_OtpVerify_Form(forms.Form):
     otp = forms.CharField(required=True, error_messages={'required':'Please enter OTP'} ,max_length=6, widget=forms.TextInput(
        attrs={'class': 'form-control'}))


class Provider_Login_Form(AuthenticationForm):
    username = forms.CharField(required=True,label="Username",widget=forms.TextInput(attrs={'class':"form-control",'placeholder':'Username','aria-label':"User Name"}))
    password = forms.CharField(required=True,label="Password",widget=forms.PasswordInput(attrs={'class':"form-control",'placeholder':'Password','aria-label':"Password"}))
    class Meta:
        model = User
        Fields = ['username','password']


class Provider_UserForm(forms.ModelForm):
    username = forms.CharField(max_length=50,disabled=True,widget=forms.TextInput(
        attrs={
            'class' : 'form-control',
        }
    ))
    email = forms.EmailField(max_length=50,disabled=True,widget=forms.EmailInput(
        attrs={
            'class' : 'form-control',
        }
    ))
    class Meta:
        model = User
        fields = ['username','email']


class Provider_ProfileForm(forms.ModelForm):
    class Meta:
        model = Provider_Profile_Model
        fields = ['avatar', 'fname', 'lname', 'tel', 'gender', 'age', 'address', 'area', 'c_name', 'c_email', 'c_website', 'c_descrip']
        widgets = {
            'avatar': forms.FileInput(attrs={
                'class':'profile_img img-fluid form-control',
                'label': 'Profile Image',
            }),
            'fname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder':'First Name',
                'label': 'First Name',
            }),
            'lname': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Last Name',
                'label': 'Last Name',
            }),
            'area': forms.Select(attrs={
                'class':'wide form-control',
                'placeholder':'Area',
                'label': 'Area',
            }),
            'gender' : forms.Select(attrs={
                'class':'wide form-control',
                'label': 'Gender',
            }),
            'age' : forms.NumberInput(attrs={
                'class':'form-control',
                'label': 'Age',
            }),
            'tel' : forms.NumberInput(attrs={
                'class':'form-control',
                'placeholder':'Phone Number',
                'label': 'Phone Number',
            }),
            'address' : forms.Textarea(attrs={
                'class':'form-control',
                'placeholder':'Address',
                'rows': 4, 'cols': 60,
                'label': 'Address',
            }),
            'c_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Company Name',
                'label': 'Company Name',
            }),
            'c_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Company Email',
                'label': 'Company Email',
            }),
            'c_website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Company Website',
                'label': 'Company Website',
            }),
            'c_descrip': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Company Description',
                'rows': 2, 'cols': 60,
                'label': 'Company Description',
            }),
        }
        labels = {
            'avatar': 'Profile Picture',
            'fname': 'First Name',
            'lname': 'Last Name',
            'tel': 'Phone Number',
            'gender': 'Gender',
            'age': 'Age',
            'address': 'Address',
            'area': 'Area',
            'c_name': 'Company Name',
            'c_email': 'Company Email',
            'c_website': 'Company Website',
            'c_descrip': 'Company Description',
        }

class ProviderProvideQuoteForm(forms.ModelForm):
    class Meta:
        model = Provide_TripQuotation
        fields = ['including_hotel', 'including_extra_activities', 'price', 'notes']
        labels = {
            'including_hotel': 'Include hotel accommodation',
            'including_extra_activities': 'Include extra activities',
            'price': 'Quoted price',
            'notes': 'Notes or comments'
        }
        widgets = {
            'including_hotel': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'transform: scale(1.8);'}),
            'including_extra_activities': forms.CheckboxInput(attrs={'class': 'form-check-input', 'style': 'transform: scale(1.8);'}),
            'price': forms.TextInput(attrs={'type': 'number', 'step': '0.01'}),
            'notes': forms.Textarea(attrs={'rows': 5,'cols': 60,})
        }
        help_texts = {
            'including_hotel': 'Check this box if your quote includes hotel accommodation.',
            'including_extra_activities': 'Check this box if your quote includes extra activities.'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['price'].required = True


class AddHotelDataForm(forms.ModelForm):
    hotel_name = forms.CharField(
        label='Hotel Name',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter hotel name'})
    )
    room_type = forms.CharField(
        label='Room Type',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter room type'})
    )
    notes = forms.CharField(
        label='Additional Notes',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter additional hotel details'})
    )
    number_of_rooms = forms.IntegerField(
        label='Number of Rooms',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter number of rooms'})
    )

    class Meta:
        model = Add_hotel_data
        fields = ['hotel_name', 'room_type','notes','number_of_rooms']
        labels = {
            'hotel_name': 'Hotel Name',
            'room_type': 'Room Type',
            'number_of_rooms': 'Will Provide Number of Rooms',
            'notes': 'Additional Hotel Details'
        }
