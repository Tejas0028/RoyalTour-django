from django.contrib import admin
from .models import *
from django.utils.translation import gettext

# Register your models here.
admin.site.register(seeker_names)
admin.site.register(Seeker_Profile_Model)

class TripQuotationAdmin(admin.ModelAdmin):
    list_display = ['customer', 'destination', 'departure_date', 'number_of_adults', 'number_of_children']
    list_filter = ['destination']
    search_fields = ['customer__fname', 'customer__lname', 'destination__name']
    date_hierarchy = 'departure_date'
    fields = ['customer', 'destination', 'departure_date', 'number_of_adults', 'number_of_children', 'notes']

admin.site.register(TripQuotation, TripQuotationAdmin)

admin.site.register(Provide_TripQuotation)

admin.site.register(Contact)