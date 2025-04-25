from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, TemplateView, RedirectView
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test # Decorator to check user permissions
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
import datetime # Import datetime module for parsing

from shows.models import Show
from bookings.models import Booking

# Helper function to check if a user is a superuser (our custom admin check)
def is_superuser(user):
    return user.is_superuser

# Apply this decorator to all custom admin views
admin_required = method_decorator(user_passes_test(is_superuser), name='dispatch')


@admin_required
class AdminDashboardView(TemplateView):
    template_name = 'custom_admin/admin_dashboard.html'


@admin_required
class AdminShowListView(ListView):
    model = Show
    template_name = 'custom_admin/shows/show_list_admin.html'
    context_object_name = 'shows'
    # Order by date/time by default, include inactive shows
    queryset = Show.objects.all().order_by('date_time')


@admin_required
@method_decorator(csrf_protect, name='post') # Protect the POST method
class AdminShowCreateView(View):
    template_name = 'custom_admin/shows/show_create_admin.html'

    def get(self, request):
        # Render the empty create form
        return render(request, self.template_name)

    def post(self, request):
        # Manual data retrieval from request.POST
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        date_str = request.POST.get('date', '').strip()
        time_str = request.POST.get('time', '').strip()
        location = request.POST.get('location', '').strip()
        total_seats_str = request.POST.get('total_seats', '').strip()
        price_str = request.POST.get('price', '').strip()
        is_active = request.POST.get('is_active') == 'on' # Check if checkbox is checked

        errors = []
        date_time = None
        total_seats = None
        price = None

        # Manual Validation
        if not title:
            errors.append("Title is required.")
        if not description:
            errors.append("Description is required.")
        if not date_str:
            errors.append("Date is required.")
        if not time_str:
            errors.append("Time is required.")
        if not location:
            errors.append("Location is required.")
        if not total_seats_str:
            errors.append("Total Seats is required.")
        if not price_str:
             errors.append("Price is required.")

        # Validate and parse date/time
        if date_str and time_str:
            try:
                # Assuming YYYY-MM-DD and HH:MM format
                datetime_str = f"{date_str} {time_str}"
                # Use a format string that matches expected input
                date_time = datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
                # Make the datetime timezone-aware (using settings.TIME_ZONE)
                date_time = timezone.make_aware(date_time, timezone.get_current_timezone())
            except ValueError:
                errors.append("Invalid date or time format. Use YYYY-MM-DD and HH:MM.")


        # Validate and parse total_seats
        if total_seats_str:
            try:
                total_seats = int(total_seats_str)
                if total_seats <= 0:
                    errors.append("Total Seats must be a positive integer.")
            except ValueError:
                errors.append("Invalid value for Total Seats.")

        # Validate and parse price
        if price_str:
             try:
                 price = float(price_str) # Use float for parsing decimal
                 if price < 0:
                     errors.append("Price cannot be negative.")
             except ValueError:
                 errors.append("Invalid value for Price.")


        if errors:
            # Re-render template with errors and submitted data
            context = {
                'errors': errors,
                'title': title,
                'description': description,
                'date_str': date_str, # Pass back individual date/time strings
                'time_str': time_str,
                'location': location,
                'total_seats_str': total_seats_str,
                'price_str': price_str,
                'is_active': is_active,
            }
            return render(request, self.template_name, context)

        # If validation passes, create the Show object
        try:
            Show.objects.create(
                title=title,
                description=description,
                date_time=date_time,
                location=location,
                total_seats=total_seats,
                # available_seats is automatically set in model's save method
                price=price,
                is_active=is_active,
            )
            # Redirect to the admin show list
            return redirect(reverse_lazy('admin_show_list'))
        except Exception as e:
             errors.append(f"An unexpected error occurred while saving: {e}")
             context = { # Pass back errors and data on unexpected save error too
                'errors': errors,
                'title': title,
                'description': description,
                'date_str': date_str,
                'time_str': time_str,
                'location': location,
                'total_seats_str': total_seats_str,
                'price_str': price_str,
                'is_active': is_active,
            }
             return render(request, self.template_name, context)


@admin_required
@method_decorator(csrf_protect, name='post') # Protect the POST method
class AdminShowUpdateView(View):
    template_name = 'custom_admin/shows/show_update_admin.html'

    def get(self, request, pk):
        # Fetch the existing show object
        show = get_object_or_404(Show, pk=pk)
        # Pass the show data to the template for pre-filling the form
        # Format date/time for HTML input type="date" and type="time"
        date_str = show.date_time.strftime('%Y-%m-%d') if show.date_time else ''
        time_str = show.date_time.strftime('%H:%M') if show.date_time else ''


        context = {
            'show': show,
            'date_str': date_str, # Pass formatted date/time strings
            'time_str': time_str,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        # Fetch the existing show object
        show = get_object_or_404(Show, pk=pk)

        # Manual data retrieval from request.POST
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        date_str = request.POST.get('date', '').strip()
        time_str = request.POST.get('time', '').strip()
        location = request.POST.get('location', '').strip()
        total_seats_str = request.POST.get('total_seats', '').strip()
        price_str = request.POST.get('price', '').strip()
        is_active = request.POST.get('is_active') == 'on' # Check if checkbox is checked

        errors = []
        date_time = None
        total_seats = None
        price = None

        # Manual Validation (similar to create view)
        if not title:
            errors.append("Title is required.")
        if not description:
            errors.append("Description is required.")
        if not date_str:
            errors.append("Date is required.")
        if not time_str:
            errors.append("Time is required.")
        if not location:
            errors.append("Location is required.")
        if not total_seats_str:
            errors.append("Total Seats is required.")
        if not price_str:
             errors.append("Price is required.")

        if date_str and time_str:
            try:
                datetime_str = f"{date_str} {time_str}"
                date_time = datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
                date_time = timezone.make_aware(date_time, timezone.get_current_timezone())
            except ValueError:
                errors.append("Invalid date or time format. Use YYYY-MM-DD and HH:MM.")

        if total_seats_str:
            try:
                total_seats = int(total_seats_str)
                if total_seats <= 0:
                    errors.append("Total Seats must be a positive integer.")
                # Important validation: Cannot reduce total seats below booked quantity
                booked_quantity = show.total_seats - show.available_seats
                if total_seats < booked_quantity:
                     errors.append(f"Cannot reduce total seats below the number of tickets already booked ({booked_quantity}).")

            except ValueError:
                errors.append("Invalid value for Total Seats.")

        if price_str:
             try:
                 price = float(price_str)
                 if price < 0:
                     errors.append("Price cannot be negative.")
             except ValueError:
                 errors.append("Invalid value for Price.")


        if errors:
            # Re-render template with errors and submitted data
            context = {
                'show': show, # Still pass the original show object
                'errors': errors,
                'title': title,
                'description': description,
                'date_str': date_str,
                'time_str': time_str,
                'location': location,
                'total_seats_str': total_seats_str,
                'price_str': price_str,
                'is_active': is_active,
            }
            return render(request, self.template_name, context)

        # If validation passes, update the Show object
        try:
            # Calculate change in available seats based on change in total seats
            old_total_seats = show.total_seats
            new_total_seats = total_seats # Use the validated integer

            # Update the show object fields
            show.title = title
            show.description = description
            show.date_time = date_time # Use the validated datetime object
            show.location = location
            show.total_seats = new_total_seats
            # Recalculate available seats based on the *change* in total seats
            # available_seats = old_available + (new_total - old_total)
            show.available_seats += (new_total_seats - old_total_seats)
            show.price = price # Use the validated float
            show.is_active = is_active

            # Ensure available_seats doesn't accidentally go below zero (should be caught by total_seats validation, but double-check)
            if show.available_seats < 0:
                 show.available_seats = 0 # Or raise a more specific error

            show.save()

            # Redirect to the admin show list
            return redirect(reverse_lazy('admin_show_list'))
        except Exception as e:
             errors.append(f"An unexpected error occurred while saving: {e}")
             context = { # Pass back errors and data on unexpected save error too
                'show': show,
                'errors': errors,
                'title': title,
                'description': description,
                'date_str': date_str,
                'time_str': time_str,
                'location': location,
                'total_seats_str': total_seats_str,
                'price_str': price_str,
                'is_active': is_active,
            }
             return render(request, self.template_name, context)


@admin_required
@method_decorator(csrf_protect, name='post') # Protect the POST method
class AdminShowDeleteView(View):
    # Using a simple POST view for deletion, often done via a form button
    # A GET confirmation page is also an option, but requires another template/view
    # Let's do a simple POST deletion.
    def post(self, request, pk):
        show = get_object_or_404(Show, pk=pk)

        # Optional: Add checks like "only delete if no bookings exist"
        if Booking.objects.filter(show=show).exists():
             # Handle error - maybe redirect back with a message
             request.session['admin_show_errors'] = [f"Cannot delete show '{show.title}' as it has associated bookings."]
             return redirect(reverse_lazy('admin_show_list'))


        show.delete()
        # Redirect back to the admin show list
        return redirect(reverse_lazy('admin_show_list'))

    def get(self, request, pk):
        # Optionally render a confirmation page
        show = get_object_or_404(Show, pk=pk)
        context = {'show': show}
        return render(request, 'custom_admin/shows/show_delete_admin.html', context)


@admin_required
class AdminBookingListView(ListView):
    model = Booking
    template_name = 'custom_admin/bookings/booking_list_admin.html'
    context_object_name = 'bookings'
    # Order by newest booking first
    queryset = Booking.objects.all().order_by('-booking_time')