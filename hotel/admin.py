from django.contrib import admin
from .models import Room, Guest, Booking, Staff

# Register your models here.

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_image' ,'room_number', 'room_type', 'price_per_night', 'capacity', 'is_available')
    list_filter = ('room_type', 'is_available')
    search_fields = ('room_number', 'room_type')

@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address','id_proof', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('guest', 'room', 'check_in', 'check_out', 'total_price', 'created_at')
    list_filter = ('created_at', 'check_in', 'check_out')
    search_fields = ('guest__user__username', 'room__room_number')
    date_hierarchy = 'created_at'
    readonly_fields = ('total_price', 'created_at', 'updated_at')

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone', 'joining_date')
    list_filter = ('role', 'joining_date')
    search_fields = ('user__username', 'user__email', 'phone')
