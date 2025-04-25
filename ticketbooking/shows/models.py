from django.db import models
from django.utils import timezone

class Show(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    total_seats = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True) # Option to hide shows

    def __str__(self):
        # Format date/time nicely for display
        local_time = timezone.localtime(self.date_time)
        formatted_date_time = local_time.strftime('%Y-%m-%d %H:%M %Z')
        return f"{self.title} ({formatted_date_time})"

    def save(self, *args, **kwargs):
        # Set available_seats on creation if not set
        if self._state.adding:
            self.available_seats = self.total_seats
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['date_time'] # Order shows by date/time by default