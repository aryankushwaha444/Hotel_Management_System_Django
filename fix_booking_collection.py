from pymongo import MongoClient

def fix_booking_collection():
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['hotel_management_db']
    
    try:
        # Drop the problematic index if it exists
        db.hotel_booking.drop_index('__primary_key__')
    except:
        pass
    
    try:
        # Drop the id index if it exists
        db.hotel_booking.drop_index('id_1')
    except:
        pass
    
    # Update all existing bookings to remove the id field
    db.hotel_booking.update_many({}, {'$unset': {'id': ""}})
    
    print("Successfully fixed booking collection")

if __name__ == '__main__':
    fix_booking_collection()
