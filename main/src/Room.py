from main.src.Booking import Booking

class Room:

    def __init__(self, room_id, room_name, room_type,  capacity, location):
        self.room_id = room_id
        self.room_name = room_name
        self.room_type = room_type
        self.capacity = capacity
        self.location = location


    def bookRoom(self, user_id, start_time, end_time):
        if self.isAvailable():# Create a booking for this room
            new_booking = Booking(user_id, self.room_id, start_time, end_time)
            return new_booking
