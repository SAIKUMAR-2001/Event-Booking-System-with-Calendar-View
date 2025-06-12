from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.safestring import mark_safe
from django.http import JsonResponse
from django.views import View
from .models import Event, Booking
from .forms import EventForm
import calendar
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def is_admin(user):
    return user.is_staff

class CalendarView(View):
    def get(self, request):
        events = Event.objects.all()
        event_list = []
        for event in events:
            event_list.append({
                "title": event.name,
                "start": event.date.isoformat(),
                "url": f"/booking/event/{event.id}/",
            })

        context = {
            "events": event_list,
        }
        return render(request, "booking/calendar.html", context)


def event_list(request):
    now = timezone.now()
    upcoming_events = Event.objects.filter(date__gte=now).order_by('date')
    past_events = Event.objects.filter(date__lt=now).order_by('-date')
    return render(request, 'booking/event_list.html', {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    })

def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    user_has_booked = False
    if request.user.is_authenticated:
        user_has_booked = Booking.objects.filter(user=request.user, event=event).exists()
    return render(request, 'booking/event_detail.html', {
        'event': event,
        'user_has_booked': user_has_booked,
    })

@login_required
def book_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if Booking.objects.filter(user=request.user, event=event).exists():
        return render(request, 'booking/event_detail.html', {
            'event': event,
            'user_has_booked': True,
            'error': 'You have already booked this event.',
        })

    if request.method == 'POST':
        Booking.objects.create(user=request.user, event=event)
        return redirect('event_detail', event_id=event.id)

    return redirect('event_detail', event_id=event.id)


@login_required
def cancel_booking(request, event_id):
    booking = get_object_or_404(Booking, user=request.user, event_id=event_id)
    if request.method == 'POST':
        booking.delete()
    return redirect('event_detail', event_id=event_id)

@user_passes_test(is_admin)
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventForm()
    return render(request, 'booking/event_form.html', {'form': form})

@user_passes_test(is_admin)
def event_edit(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventForm(instance=event)
    return render(request, 'booking/event_form.html', {'form': form})

@user_passes_test(is_admin)
def event_delete(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    return render(request, 'booking/event_confirm_delete.html', {'event': event})

@user_passes_test(is_admin)
def view_attendees(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    bookings = event.booking_set.all()
    return render(request, 'booking/attendees_list.html', {
        'event': event,
        'bookings': bookings,
    })
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after signup
            return redirect('event_list')
    else:
        form = UserCreationForm()
    return render(request, 'booking/signup.html', {'form': form})