from django.contrib import admin
from .models import Event, Booking

class BookingInline(admin.TabularInline):
    model = Booking
    extra = 0
    readonly_fields = ['booking_date']
    can_delete = False

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'max_participants', 'available_slots']
    list_filter = ['date']
    search_fields = ['name', 'description']
    inlines = [BookingInline]
    readonly_fields = ['created_at', 'updated_at', 'available_slots']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'booking_date']
    list_filter = ['event', 'booking_date']
    search_fields = ['user__username', 'event__name']
    readonly_fields = ['booking_date']