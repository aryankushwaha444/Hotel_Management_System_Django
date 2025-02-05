from pymongo import MongoClient
from datetime import datetime
import os

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['hotel_management_db']
room_collection = db['hotel_room']

# Ensure media directory exists
media_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'room_images')
os.makedirs(media_dir, exist_ok=True)

# Sample room data with images
rooms = [
    {
        "id": 1,
        "room_number": "101",
        "room_type": "Single",
        "capacity": 1,
        "price_per_night": 2500.00,
        "description": """Cozy single room perfect for solo travelers or business professionals.
Features:
- Queen-size bed with premium mattress
- Work desk with ergonomic chair
- 32-inch Smart TV
- Private bathroom with shower
- Free Wi-Fi
- Air conditioning
- Mini fridge
- Tea/coffee maker""",
        "image_path": "room_images/single_room_101.jpg",
        "amenities": [
            "Queen bed",
            "Work desk",
            "Smart TV",
            "Private bathroom",
            "Wi-Fi",
            "Air conditioning",
            "Mini fridge",
            "Tea/coffee maker"
        ],
        "is_available": True,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": 2,
        "room_number": "102",
        "room_type": "Double",
        "capacity": 2,
        "price_per_night": 3500.00,
        "description": """Spacious double room ideal for couples or friends traveling together.
Features:
- Two double beds with luxury linens
- Seating area with sofa
- 40-inch Smart TV
- Private bathroom with bathtub
- Free high-speed Wi-Fi
- Climate control
- Mini bar
- Coffee machine
- Work desk""",
        "image_path": "room_images/double_room_102.jpg",
        "amenities": [
            "Two double beds",
            "Seating area",
            "Smart TV",
            "Bathtub",
            "High-speed Wi-Fi",
            "Climate control",
            "Mini bar",
            "Coffee machine",
            "Work desk"
        ],
        "is_available": True,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": 3,
        "room_number": "201",
        "room_type": "Suite",
        "capacity": 4,
        "price_per_night": 6000.00,
        "description": """Luxury suite with panoramic city views, perfect for families or extended stays.
Features:
- Master bedroom with king-size bed
- Separate living room with sofa bed
- Two 55-inch Smart TVs
- Luxury bathroom with jacuzzi
- Walk-in closet
- Full kitchenette
- Dining area
- Private balcony
- Premium Wi-Fi
- Smart home controls""",
        "image_path": "room_images/luxury_suite_201.jpg",
        "amenities": [
            "King bed",
            "Living room",
            "Two Smart TVs",
            "Jacuzzi",
            "Walk-in closet",
            "Kitchenette",
            "Dining area",
            "Balcony",
            "Premium Wi-Fi",
            "Smart controls"
        ],
        "is_available": True,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": 4,
        "room_number": "202",
        "room_type": "Double",
        "capacity": 2,
        "price_per_night": 3500.00,
        "description": """Contemporary double room with modern design and city views.
Features:
- Two queen-size beds
- Modern furnishings
- 42-inch Smart TV
- Rainfall shower
- Free Wi-Fi
- Climate control
- Mini fridge
- Coffee maker
- Work space""",
        "image_path": "room_images/double_room_202.jpg",
        "amenities": [
            "Two queen beds",
            "Modern design",
            "Smart TV",
            "Rainfall shower",
            "Wi-Fi",
            "Climate control",
            "Mini fridge",
            "Coffee maker",
            "Work space"
        ],
        "is_available": True,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": 5,
        "room_number": "301",
        "room_type": "Suite",
        "capacity": 3,
        "price_per_night": 5500.00,
        "description": """Executive suite with premium amenities and stunning views.
Features:
- Master bedroom with king-size bed
- Living area with pull-out sofa
- 50-inch Smart TV
- Luxury bathroom with double vanity
- Executive work desk
- Mini kitchen
- Espresso machine
- Private balcony
- High-speed Wi-Fi
- Room service""",
        "image_path": "room_images/executive_suite_301.jpg",
        "amenities": [
            "King bed",
            "Living area",
            "Smart TV",
            "Luxury bathroom",
            "Work desk",
            "Mini kitchen",
            "Espresso machine",
            "Balcony",
            "High-speed Wi-Fi",
            "Room service"
        ],
        "is_available": True,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
        {
        "id": 6,
        "room_number": "302",
        "room_type": "Deluxe",
        "capacity": 2,
        "price_per_night": 4500.00,
        "description": """Spacious deluxe room with modern amenities and elegant decor.
Features:
- Queen-size bed
- Cozy seating area
- 42-inch Smart TV
- Stylish bathroom with walk-in shower
- Work desk with ergonomic chair
- Tea/coffee maker
- Private balcony with city view
- High-speed Wi-Fi
- 24/7 room service""",
        "image_path": "room_images/deluxe_room_302.jpg",
        "amenities": [
            "Queen bed",
            "Seating area",
            "Smart TV",
            "Walk-in shower",
            "Work desk",
            "Tea/coffee maker",
            "Balcony",
            "High-speed Wi-Fi",
            "24/7 Room service"
        ],
        "is_available": True,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": 7,
        "room_number": "303",
        "room_type": "Deluxe",
        "capacity": 2,
        "price_per_night": 4500.00,
        "description": """Elegant deluxe room with comfort and luxury amenities.
Features:
- King-size bed
- Comfortable lounge chair
- 42-inch Smart TV
- Stylish bathroom with bathtub
- Work desk with reading lamp
- Tea/coffee maker
- Private balcony with city view
- High-speed Wi-Fi
- 24/7 room service""",
        "image_path": "room_images/deluxe_room_303.jpg",
        "amenities": [
            "King bed",
            "Lounge chair",
            "Smart TV",
            "Bathtub",
            "Work desk",
            "Tea/coffee maker",
            "Balcony",
            "High-speed Wi-Fi",
            "24/7 Room service"
        ],
        "is_available": True,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
]

def import_rooms():
    try:
        # Delete existing rooms (optional)
        room_collection.delete_many({})
        
        # Insert new rooms
        result = room_collection.insert_many(rooms)
        print(f"Successfully inserted {len(result.inserted_ids)} rooms")
        
        # Verify the insertion
        print("\nInserted rooms:")
        for room in room_collection.find():
            print(f"\nRoom {room['room_number']}: {room['room_type']} - ₹{room['price_per_night']}/night")
            print(f"Image: {room['image_path']}")
            print("Amenities:", ", ".join(room['amenities']))
            
    except Exception as e:
        print("Error importing rooms:", str(e))

def get_rooms():
    try:
        print("\nAll rooms in database:")
        for room in room_collection.find():
            print(f"\nRoom {room['room_number']}: {room['room_type']} - ₹{room['price_per_night']}/night")
            print(f"Image: {room['image_path']}")
            print("Amenities:", ", ".join(room['amenities']))
    except Exception as e:
        print("Error getting rooms:", str(e))

if __name__ == '__main__':
    print("Importing rooms...")
    import_rooms()
    print("\nFetching all rooms...")
    get_rooms()
