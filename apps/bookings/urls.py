from django.urls import path
from .import views



urlpatterns = [
    path('book-vehicle', views.BookVehicleView.as_view(), name="book_vehicle"),
    path('bookings', views.UserBookingsListView.as_view(), name="bookings")
]
