from django.contrib import admin
from .models import *
from seeker.models import Add_hotel_data

admin.site.register(provider_names)

@admin.register(Provider_Profile_Model)
class Provider_Profile_Model_Admin(admin.ModelAdmin):
    list_display = ('user', 'fname', 'lname', 'tel', 'gender', 'age', 'address', 'area')


@admin.register(city_data)
class CityDataAdmin(admin.ModelAdmin):
    list_display = ('city', 'state_name')
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('city')


class AddHotelDataAdmin(admin.ModelAdmin):
    list_display = ('trip_quotation', 'hotel_name', 'room_type')
    list_filter = ('hotel_name',)
    search_fields = ('trip_quotation__destination', 'hotel_name')

admin.site.register(Add_hotel_data, AddHotelDataAdmin)
