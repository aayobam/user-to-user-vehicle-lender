from django.urls import path
from .import views


urlpatterns = [
    path('book-vehicle/<str:vehicle_id>', views.BookVehicleView.as_view(), name="book_vehicle"),
    path('orders', views.OrdersListView.as_view(), name="order_list"),
    path('my-bookings', views.BookingListView.as_view(), name="booking_list"),
    path('update-booking/<str:id>', views.UpdateBookingView.as_view(), name="update_booking"),
    path('update-order/<str:id>', views.UpdateOrderView.as_view(), name="update_order"),
    path('cancel-order/<str:id>', views.CancelBookingView.as_view(), name="cancel_booking")
]
