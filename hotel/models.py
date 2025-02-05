from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime

# Create your models here.

class Room(models.Model):
    ROOM_TYPES = (
        ('Single', 'Single'),
        ('Double', 'Double'),
        ('Suite', 'Suite'),
        ('Deluxe', 'Deluxe'),
    )
    
    room_image = models.ImageField(upload_to='room_images/', null=True, blank=True)
    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField()
    description = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.room_number} - {self.room_type}"

class Guest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    id_proof = models.CharField(max_length=20)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.get_full_name() or self.user.username

class Booking(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    payment_status = models.CharField(max_length=20, default='pending')

    def save(self, *args, **kwargs):
        if not self.total_price:
            # Convert string dates to datetime if they aren't already
            if isinstance(self.check_in, str):
                self.check_in = datetime.fromisoformat(self.check_in)
            if isinstance(self.check_out, str):
                self.check_out = datetime.fromisoformat(self.check_out)
                
            # Calculate total price based on number of nights and room price
            nights = (self.check_out - self.check_in).days
            self.total_price = self.room.price_per_night * nights
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.guest.user.username} - {self.room.room_number} ({self.check_in} to {self.check_out})"

class Staff(models.Model):
    ROLES = (
        ('Manager', 'Manager'),
        ('Receptionist', 'Receptionist'),
        ('Housekeeper', 'Housekeeper'),
        ('Maintenance', 'Maintenance'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLES)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    joining_date = models.DateField(default=timezone.now)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.role}"
