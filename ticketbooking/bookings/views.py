from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin # Require user to be logged in

from .models import Booking

class BookingHistoryView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'bookings/booking_history.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        # Return only bookings for the current logged-in user
        return Booking.objects.filter(user=self.request.user).order_by('-booking_time')


class BookingConfirmationView(TemplateView):
    template_name = 'bookings/booking_confirmation.html'
    # This is a simple success page. Could be enhanced to show booking details
    # by passing the booking ID in the redirect URL and fetching it here.