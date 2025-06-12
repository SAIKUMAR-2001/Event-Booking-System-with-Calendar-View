from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    max_participants = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def available_slots(self):
        return self.max_participants - self.booking_set.count()

    def is_fully_booked(self):
        return self.available_slots <= 0

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.event.name}"

    def clean(self):
        # Prevent duplicate bookings
        if Booking.objects.filter(user=self.user, event=self.event).exists():
            raise ValidationError("You have already booked this event.")
        
        # Check if event is fully booked
        if self.event.is_fully_booked():
            raise ValidationError("This event is fully booked.")
        
        # Check if event date is in the past
        if self.event.date < timezone.now():
            raise ValidationError("Cannot book past events.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)