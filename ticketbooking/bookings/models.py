from django.db import models
from django.contrib.auth.models import User
from shows.models import Show # Import Show model
from django.utils import timezone

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='bookings')
    quantity = models.PositiveIntegerField()
    booking_time = models.DateTimeField(default=timezone.now) # Use timezone.now()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Booking for {self.show.title} by {self.user.username} ({self.quantity} tickets)"

    class Meta:
        ordering = ['-booking_time'] # Order by newest booking first