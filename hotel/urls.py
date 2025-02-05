from django.urls import path
from . import views
from .views import BookingListView, BookingDetailView, StaffDashboardView

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('rooms/', views.room_list, name='room_list'),
    path('room/<str:room_id>/', views.room_detail, name='room_detail'),
    path('room/<str:room_id>/book/', views.book_room, name='book_room'),
    path('bookings/', views.booking_list, name='booking_list'),
    path('booking/<str:booking_id>/', views.booking_detail, name='booking_detail'),
    path('booking/<str:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('staff/dashboard/', StaffDashboardView.as_view(), name='staff_dashboard'),
    path('staff/booking/<str:booking_id>/', views.manage_booking, name='manage_booking'),
]
