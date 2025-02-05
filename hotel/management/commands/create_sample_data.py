from django.core.management.base import BaseCommand
from hotel.models import Room
from decimal import Decimal

class Command(BaseCommand):
    help = 'Creates sample rooms for testing'

    def handle(self, *args, **kwargs):
        # Sample room data
        rooms = [
            {
                'room_number': '101',
                'room_type': 'Single',
                'price_per_night': Decimal('100.00'),
                'capacity': 1,
                'description': 'Cozy single room with a comfortable bed, private bathroom, and city view.',
                'is_available': True
            },
            {
                'room_number': '102',
                'room_type': 'Double',
                'price_per_night': Decimal('150.00'),
                'capacity': 2,
                'description': 'Spacious double room with two beds, private bathroom, and garden view.',
                'is_available': True
            },
            {
                'room_number': '201',
                'room_type': 'Suite',
                'price_per_night': Decimal('250.00'),
                'capacity': 3,
                'description': 'Luxury suite with separate living area, king-size bed, and panoramic city view.',
                'is_available': True
            },
            {
                'room_number': '202',
                'room_type': 'Deluxe',
                'price_per_night': Decimal('300.00'),
                'capacity': 4,
                'description': 'Premium deluxe room with modern amenities, balcony, and mountain view.',
                'is_available': True
            }
        ]

        for room_data in rooms:
            Room.objects.create(**room_data)
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created room {room_data["room_number"]}')
            )
