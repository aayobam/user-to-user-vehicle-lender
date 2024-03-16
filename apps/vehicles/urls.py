from django.urls import path
from .import views


urlpatterns = [
    path('add-vehicle', views.CreateVehicleView.as_view(), name="add_vehicle"),
    path('my-vehicles', views.ListVehicleView.as_view(), name="my_vehicles"),
    path('search-vehicle', views.SearchVehicleView.as_view(), name="search_vehicle"),
    path('search-results', views.SearchResultView.as_view(), name="search_results")
]
