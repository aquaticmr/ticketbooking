from django.urls import path
from .views import BookingHistoryView, BookingConfirmationView

urlpatterns = [
    path('history/', BookingHistoryView.as_view(), name='booking_history'),
    path('confirmation/', BookingConfirmationView.as_view(), name='booking_confirmation'),
]