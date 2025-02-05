from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Room, Booking, Guest, Staff
from django.utils import timezone
from .forms import UserRegistrationForm, GuestForm
from django.contrib.auth import login
from datetime import datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RoomSerializer
from pymongo import MongoClient
from bson import ObjectId

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                # First try to connect to MongoDB before creating the user
                client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
                # Test the connection
                client.server_info()
                
                # Save user to Django's default database
                user = form.save()
                
                # Create guest profile in Django
                guest = Guest.objects.create(
                    user=user,
                    phone=form.cleaned_data['phone_number'],
                    address='',  # Can be updated later in profile
                    id_proof=''  # Can be updated later in profile
                )
                
                db = client['hotel_management_db']
                users_collection = db['users']
                
                # Prepare user data for MongoDB
                user_data = {
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'phone_number': form.cleaned_data['phone_number'],
                    'date_joined': user.date_joined.isoformat(),
                    'is_active': user.is_active,
                    'django_id': str(user.id),  # Reference to Django user ID
                    'created_at': datetime.now()
                }
                
                # Insert user data into MongoDB
                result = users_collection.insert_one(user_data)
                
                if not result.inserted_id:
                    raise Exception("Failed to insert user data into MongoDB")
                
                login(request, user)
                messages.success(request, 'Registration successful! Welcome to our hotel.')
                return redirect('profile')
                
            except Exception as e:
                # If anything fails, cleanup and show error
                if 'user' in locals():
                    user.delete()  # Delete the user if it was created
                if 'guest' in locals():
                    guest.delete()  # Delete the guest profile if it was created
                    
                error_message = str(e)
                if "Connection refused" in error_message:
                    messages.error(request, 'Registration failed: Could not connect to the database. Please try again later.')
                else:
                    messages.error(request, f'Registration failed: {error_message}')
                print(f'Registration Error: {error_message}')
                
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})

@login_required
def room_list(request):
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['hotel_management_db']
    room_collection = db['hotel_room']
    
    # Get filter parameters
    room_type = request.GET.get('room_type')
    
    # Build query
    query = {}
    if room_type:
        query['room_type'] = room_type
    
    # Get rooms from MongoDB
    rooms = list(room_collection.find(query))
    
    # Convert ObjectId to string for each room and ensure it's stored in both id and _id
    valid_rooms = []
    for room in rooms:
        if '_id' in room:
            room['id'] = str(room['_id'])
            valid_rooms.append(room)
            print(f"Room ID: {room['id']}")  # Debug print
    
    return render(request, 'hotel/room_list.html', {'rooms': valid_rooms})

@login_required
def room_detail(request, room_id):
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['hotel_management_db']
    room_collection = db['hotel_room']
    
    # Get room from MongoDB using ObjectId
    room = room_collection.find_one({'_id': ObjectId(room_id)})
    
    if not room:
        messages.error(request, 'Room not found')
        return redirect('room_list')
    
    # Convert ObjectId to string for template
    room['id'] = str(room['_id'])
    
    return render(request, 'hotel/room_detail.html', {'room': room})

@login_required
def book_room(request, room_id):
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['hotel_management_db']
    room_collection = db['hotel_room']
    booking_collection = db['hotel_booking']
    
    # Get room from MongoDB
    room = room_collection.find_one({'_id': ObjectId(room_id)})
    if not room:
        messages.error(request, 'Room not found')
        return redirect('room_list')
    
    # Convert ObjectId to string for template
    room['id'] = str(room['_id'])
    
    if request.method == 'POST':
        try:
            # Convert string dates to datetime objects
            check_in = datetime.fromisoformat(request.POST['check_in'].replace('T', ' '))
            check_out = datetime.fromisoformat(request.POST['check_out'].replace('T', ' '))

            # Validate dates
            if check_in >= check_out:
                messages.error(request, 'Check-out date must be after check-in date')
                return redirect('book_room', room_id=room_id)

            # Check if room is already booked for these dates
            # existing_booking = booking_collection.find_one({
            #     'room_id': ObjectId(room_id),
            #     'status': 'confirmed',
            #     '$or': [
            #         {
            #             'check_in': {'$lt': check_out},
            #             'check_out': {'$gt': check_in}
            #         }
            #     ]
            # })

            # if existing_booking:
            #     messages.error(request, 'Room is already booked for these dates')
            #     return redirect('book_room', room_id=room_id)

            # Create booking document with auto-generated ObjectId
            booking = {
                '_id': ObjectId(),  # MongoDB will handle the unique ID
                'room_id': ObjectId(room_id),
                'user_id': request.user.id,
                'guest_name': f"{request.user.first_name} {request.user.last_name}",
                'check_in': check_in,
                'check_out': check_out,
                'status': 'confirmed',
                'created_at': datetime.now(),
                'total_price': room['price_per_night'] * (check_out - check_in).days,
                'room_number': room['room_number'],
                'room_type': room['room_type'],
                'payment_status': 'pending',
                'payment_method': 'cash',
                'updated_at': datetime.now()
            }
            
            # Insert booking into MongoDB
            result = booking_collection.insert_one(booking)
            
            # Update room availability
            room_collection.update_one(
                {'_id': ObjectId(room_id)},
                {'$set': {'is_available':False}}
            )
            
            messages.success(request, 'Room booked successfully!')
            return redirect('booking_detail', booking_id=str(result.inserted_id))
            
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('room_list')
    
    return render(request, 'hotel/book_room.html', {'room': room})

@login_required
def booking_list(request):
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['hotel_management_db']
    booking_collection = db['hotel_booking']
    room_collection = db['hotel_room']
    
    # Get all bookings for the current user
    bookings = list(booking_collection.find({'user_id': request.user.id}))
    
    # Add room details and convert ObjectIds to strings
    for booking in bookings:
        booking['id'] = str(booking['_id'])
        room = room_collection.find_one({'_id': booking['room_id']})
        if room:
            booking['room'] = room
            booking['room']['id'] = str(room['_id'])
    
    return render(request, 'hotel/booking_list.html', {'bookings': bookings})

@login_required
def booking_detail(request, booking_id):
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['hotel_management_db']
    booking_collection = db['hotel_booking']
    room_collection = db['hotel_room']
    
    # Get booking from MongoDB
    booking = booking_collection.find_one({'_id': ObjectId(booking_id)})
    if not booking:
        messages.error(request, 'Booking not found')
        return redirect('booking_list')
    
    # Add room details and convert ObjectIds to strings
    booking['id'] = str(booking['_id'])
    room = room_collection.find_one({'_id': booking['room_id']})
    if room:
        booking['room'] = room
        booking['room']['id'] = str(room['_id'])
    
    return render(request, 'hotel/booking_detail.html', {'booking': booking})

@login_required
def cancel_booking(request, booking_id):
    if request.method != 'POST':
        return redirect('booking_detail', booking_id=booking_id)
    
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['hotel_management_db']
    booking_collection = db['hotel_booking']
    room_collection = db['hotel_room']
    
    # Get booking from MongoDB
    booking = booking_collection.find_one({'_id': ObjectId(booking_id)})
    if not booking:
        messages.error(request, 'Booking not found')
        return redirect('booking_list')
    
    # Check if the booking belongs to the current user
    if booking['user_id'] != request.user.id:
        messages.error(request, 'You are not authorized to cancel this booking')
        return redirect('booking_list')
    
    # Update booking status
    booking_collection.update_one(
        {'_id': ObjectId(booking_id)},
        {'$set': {'payment_status': 'cancelled',
                  'payment_method':'N/A'}}
    )
    
    # Make room available again
    room_collection.update_one(
        {'_id': booking['room_id']},
        {'$set': {'is_available': True}}
        
    )
    
    messages.success(request, 'Booking cancelled successfully')
    return redirect('booking_list')

class BookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'hotel/booking_list.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return Booking.objects.filter(guest__user=self.request.user)

class BookingDetailView(LoginRequiredMixin, DetailView):
    model = Booking
    template_name = 'hotel/booking_detail.html'

@login_required
def profile_view(request):
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['hotel_management_db']
    booking_collection = db['hotel_booking']
    room_collection = db['hotel_room']
    
    # Get recent bookings for the current user
    recent_bookings = list(booking_collection.find(
        {'user_id': request.user.id}
    ).sort('created_at', -1).limit(5))  # Get last 5 bookings
    
    # Add room details and convert ObjectIds to strings
    for booking in recent_bookings:
        booking['id'] = str(booking['_id'])
        room = room_collection.find_one({'_id': booking['room_id']})
        if room:
            booking['room'] = room
            booking['room']['id'] = str(room['_id'])
    
    context = {
        'user': request.user,
        'recent_bookings': recent_bookings
    }
    
    return render(request, 'hotel/profile.html', context)

# Staff views
class StaffDashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Booking
    template_name = 'hotel/staff_dashboard.html'
    context_object_name = 'bookings'

    def test_func(self):
        return hasattr(self.request.user, 'staff')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_bookings'] = Booking.objects.count()
        context['recent_bookings'] = Booking.objects.order_by('-created_at')[:5]
        return context

@login_required
def manage_booking(request, booking_id):
    if not hasattr(request.user, 'staff'):
        messages.error(request, 'Access denied')
        return redirect('dashboard')

    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'confirm':
            booking.status = 'confirmed'
        elif action == 'cancel':
            booking.status = 'cancelled'
            booking.payment_status = 'cancelled'
        booking.save()
        messages.success(request, f'Booking {booking.status}')
        return redirect('staff_dashboard')
    
    return render(request, 'hotel/manage_booking.html', {'booking': booking})

def dashboard(request):
    return render(request, 'hotel/dashboard.html')

@api_view(['GET'])
def room_list_api(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)
