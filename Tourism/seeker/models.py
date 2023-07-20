from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django_resized import ResizedImageField
from django.utils.translation import gettext_lazy as _
from provider.models import Provider_Profile_Model, city_data, state_data
from Tours.models import Destination

# Create your models here.


GENDER = (
    ('Select','Select'),
    ('Male','Male'),
    ('Female','Female')
)

class seeker_names(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Seeker_Profile_Model(models.Model):
    user = models.OneToOneField(seeker_names, on_delete=models.CASCADE,primary_key=True)
    avatar = ResizedImageField(size=[450, 450], crop=['middle','center'],upload_to="seeker_profile/",null=True,blank=True, default="/seeker_profile/avatar.jpeg")
    fname = models.CharField(max_length=50,null=True,blank=True)
    lname = models.CharField(max_length=50,null=True,blank=True)
    tel = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER, default='M')
    age = models.IntegerField(default=15, null=True, blank=True)
    address = models.TextField(max_length=300, null=True, blank=True)
    area = models.ForeignKey(city_data,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return str(self.user)

@receiver(post_save, sender=seeker_names)
def create_Seeker_Profile_Model(sender, instance, created, **kwargs):
    if created:
        Seeker_Profile_Model.objects.create(user=instance)

@receiver(post_save, sender=seeker_names)
def save_user_Seeker_Profile_Model(sender, instance, **kwargs):
    instance.seeker_profile_model.save()

class TripQuotation(models.Model):
    customer = models.ForeignKey(seeker_names,on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination,on_delete=models.CASCADE)
    departure_date = models.DateField()
    number_of_adults = models.IntegerField()
    number_of_children = models.IntegerField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return str(self.destination)

class Provide_TripQuotation(models.Model):
    trip_quotation = models.ForeignKey(TripQuotation, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider_Profile_Model, on_delete=models.CASCADE)
    including_hotel = models.BooleanField()
    including_extra_activities = models.BooleanField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Quote for {self.trip_quotation.destination} provided by {self.provider}"

class Add_hotel_data(models.Model):
    trip_quotation = models.ForeignKey(TripQuotation, on_delete=models.CASCADE)
    hotel_name = models.CharField(max_length=255)
    room_type = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    number_of_rooms = models.IntegerField()

    def __str__(self):
        return f"{self.hotel_name} for {self.trip_quotation.customer}"

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)