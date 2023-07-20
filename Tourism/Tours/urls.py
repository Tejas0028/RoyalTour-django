from django.urls import path
from .views import *

app_name = "Tour"

urlpatterns = [
    path('add_destination/',create_destination,name="add_destination"),
    path('manage_destinations/',manage_destinations,name="manage_destinations"),
    path('destination/<int:destination_id>/', destination_detail, name='destination_detail'),
    path('destination_edit/<int:destination_id>/',destination_edit,name="destination_edit"),
    path('destination_delete/<int:destination_id>/',destination_delete,name="destination_delete")

]
