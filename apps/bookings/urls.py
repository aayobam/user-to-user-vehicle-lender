from django.urls import path
from .import views


urlpatterns = [
    path('book-vehicle', views.BookVehicleView.as_view(), name="book_vehicle"),
    path('my-bookings', views.OwnerBookingListView.as_view(), name="owner_bookings"),
    path('orders', views.CustomerBookingListView.as_view(), name="customer_bookings"),
]
