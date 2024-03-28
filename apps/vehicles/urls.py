from django.urls import path
from .import views


urlpatterns = [
    path('add-vehicle', views.CreateVehicleView.as_view(), name="add_vehicle"),
    path('my-vehicles', views.VehicleListView.as_view(), name="vehicle_list"),
    path('vehicle-detail/<str:id>',
         views.VehicleDetailView.as_view(), name="vehicle_detail"),
    path('update-vehicle/<str:id>',
         views.UpdateVehicleView.as_view(), name="update_vehicle"),
    path('delete-vehicle/<str:id>',
         views.DeleteVehicleView.as_view(), name="delete_vehicle")
]
