from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin # Useful mixin for CBVs
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.utils import timezone # Import timezone module

from .models import Show
from bookings.models import Booking # Import Booking model from bookings app

class ShowListView(ListView):
    model = Show
    template_name = 'shows/show_list.html'
    context_object_name = 'shows'
    # Only show active shows in the public list
    queryset = Show.objects.filter(is_active=True).order_by('date_time')

@method_decorator(csrf_protect, name='post') # Protect the POST method
class ShowDetailView(DetailView):
    model = Show
    template_name = 'shows/show_detail.html'
    context_object_name = 'show'
    pk_url_kwarg = 'pk' # Ensure the URL pattern passes the primary key as 'pk'

    def get_queryset(self):
        # Ensure only active shows are viewable publicly
        return Show.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass any errors from POST request back to the template
        context['errors'] = self.request.session.pop('booking_errors', [])
        context['submitted_quantity'] = self.request.session.pop('booking_quantity', '')
        return context


    def post(self, request, *args, **kwargs):
        # Handle booking logic here
        self.object = self.get_object() # Get the show object
        show = self.object

        # Ensure user is logged in
        if not request.user.is_authenticated:
            # Store attempted quantity in session to pre-fill if they log in
            request.session['booking_quantity'] = request.POST.get('quantity', '')
            # Redirect to login, preserving the current page in 'next' parameter
            return redirect(f'{reverse("login")}?next={request.get_full_path()}')


        # Manual data retrieval and validation from request.POST
        quantity_str = request.POST.get('quantity')
        errors = []
        quantity = 0

        if not quantity_str:
            errors.append("Please enter the number of tickets.")
        else:
            try:
                quantity = int(quantity_str)
                if quantity <= 0:
                    errors.append("Quantity must be a positive number.")
            except ValueError:
                errors.append("Invalid quantity entered.")

        if not errors: # Only perform seat check if quantity is valid number
            if quantity > show.available_seats:
                errors.append(f"Only {show.available_seats} seats available.")
            if quantity > show.total_seats: # Should not happen if quantity > 0, but good check
                 errors.append(f"Cannot book more than total seats available ({show.total_seats}).")

        if errors:
            # Store errors and submitted quantity in session and redirect back to the detail page
            request.session['booking_errors'] = errors
            request.session['booking_quantity'] = quantity_str
            return redirect(reverse('show_detail', kwargs={'pk': show.pk})) # Redirect to GET

        # If validation passes, create the booking
        try:
            # Use a database transaction for atomicity (optional but recommended for real systems)
            # from django.db import transaction
            # with transaction.atomic():

            # Double-check availability just before saving (optimistic locking check)
            # Reload show from DB to get latest available_seats
            show.refresh_from_db()
            if quantity > show.available_seats:
                 # This can happen in high concurrency, handle again
                 request.session['booking_errors'] = ["Sorry, available seats changed. Please try again."]
                 request.session['booking_quantity'] = quantity_str
                 return redirect(reverse('show_detail', kwargs={'pk': show.pk}))


            total_price = quantity * show.price

            booking = Booking.objects.create(
                user=request.user,
                show=show,
                quantity=quantity,
                total_price=total_price,
                booking_time=timezone.now() # Use timezone.now()
            )

            # Update show's available seats
            show.available_seats -= quantity
            show.save()

            # Redirect to a confirmation page or booking history
            # We can pass booking ID to confirmation page if needed
            return redirect(reverse('booking_confirmation')) # Redirect to GET for confirmation

        except Exception as e:
            errors.append(f"An unexpected error occurred during booking: {e}")
            request.session['booking_errors'] = errors
            request.session['booking_quantity'] = quantity_str
            return redirect(reverse('show_detail', kwargs={'pk': show.pk}))