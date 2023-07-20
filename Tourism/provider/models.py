from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django_resized import ResizedImageField
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from seeker.models import *

# Create your models here.


GENDER = (
    ('Select','Select'),
    ('Male','Male'),
    ('Female','Female')
)

class state_data(models.Model):
    state = models.CharField(max_length=200)

    def __str__(self):
        return str(self.state)

class city_data(models.Model):
    state_name = models.ForeignKey(state_data,max_length=200,on_delete=models.PROTECT)
    city = models.CharField(max_length=200)

    def __str__(self):
        return self.city

class provider_names(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Provider_Profile_Model(models.Model):
    user = models.OneToOneField(provider_names, on_delete=models.CASCADE,primary_key=True)
    avatar = ResizedImageField(size=[450, 450], crop=['middle','center'],upload_to="provider_profile/",null=True,blank=True, default="/provider_profile/default.png")
    fname = models.CharField(max_length=50,null=True,blank=True)
    lname = models.CharField(max_length=50,null=True,blank=True)
    tel = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER, default='M')
    age = models.IntegerField(default=15, null=True, blank=True)
    address = models.TextField(max_length=300, null=True, blank=True)
    area = models.ForeignKey(city_data,on_delete=models.CASCADE,null=True,blank=True)
    c_name = models.CharField(max_length=50,null=True,blank=True)
    c_email = models.CharField(max_length=50,null=True,blank=True)
    c_website = models.CharField(max_length=50,null=True,blank=True)
    c_descrip = models.TextField(max_length=500,null=True,blank=True)

    def __str__(self):
        return str(self.user)

@receiver(post_save, sender=provider_names)
def create_Provider_Profile_Model(sender, instance, created, **kwargs):
    if created:
        Provider_Profile_Model.objects.create(user=instance)

@receiver(post_save, sender=provider_names)
def save_user_Provider_Profile_Model(sender, instance, **kwargs):
    instance.provider_profile_model.save()
