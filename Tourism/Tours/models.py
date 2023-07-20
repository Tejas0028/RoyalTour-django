from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from provider.models import *

class Destination(models.Model):
    """
    Model representing a travel destination.
    """
    provider = models.ForeignKey(provider_names,on_delete=models.CASCADE)
    name = models.CharField(max_length=100, help_text="Enter the name of the destination.")
    description = models.TextField(help_text="Enter a description of the destination.")
    image = models.ImageField(upload_to="destination_images/", help_text="Upload an image of the destination.")
    country = models.ForeignKey(state_data, on_delete=models.CASCADE, help_text="Select the state where the destination is located.")
    city = models.ForeignKey(city_data, on_delete=models.CASCADE, help_text="Select the city where the destination is located.")
    climate = models.CharField(max_length=100, help_text="Enter the climate of the destination.")
    language = models.CharField(max_length=100, help_text="Enter the primary language spoken in the destination.")
    currency = models.CharField(max_length=100, help_text="Enter the currency used in the destination.")
    timezone = models.CharField(max_length=100, help_text="Enter the timezone of the destination.")
    days = models.IntegerField(null=True,blank=True , help_text="Days")
    nights = models.IntegerField(null=True,blank=True , help_text="Nights")
    is_popular = models.BooleanField(default=False, help_text="Check if the destination is popular among travelers.")
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    itinerary = models.TextField(help_text="Enter a description of the destination.")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

@receiver(pre_save, sender=Destination)
def update_city(sender, instance, *args, **kwargs):
    """
    Automatically update the country based on the selected city.
    """
    if instance.city.state_name != instance.country:
        instance.country = instance.city.state_name

