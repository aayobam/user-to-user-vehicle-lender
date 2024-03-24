from django.urls import path
from .import views


urlpatterns = [
    path('add-vehicle', views.CreateVehicleView.as_view(), name="add_vehicle"),
    path('my-vehicles', views.ListVehicleView.as_view(), name="my_vehicles"),
]
