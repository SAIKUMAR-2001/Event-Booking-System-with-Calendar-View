from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from .views import CalendarView


urlpatterns = [
     path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='booking/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='event_list'), name='logout'),
    path('', views.event_list, name='event_list'),
   path('calendar/', CalendarView.as_view(), name='calendar'),
   path('event/<int:event_id>/', views.event_detail, name='event_detail'),

    path('calendar/<int:year>/<int:month>/', views.CalendarView.as_view(), name='calendar_month'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('event/<int:event_id>/book/', views.book_event, name='book_event'),
    path('event/<int:event_id>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('event/create/', views.event_create, name='event_create'),
    path('event/<int:event_id>/edit/', views.event_edit, name='event_edit'),
    path('event/<int:event_id>/delete/', views.event_delete, name='event_delete'),
    path('event/<int:event_id>/attendees/', views.view_attendees, name='view_attendees'),
]