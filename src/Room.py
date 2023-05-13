from Booking import *

class Room:
    def __init__(self, room_id, rate, capacity):
        self.room_id = room_id
        self.rate = rate
        self.capacity = capacity

    def bookRoom(self, user_id, start_time, end_time):
        # Create a booking for this room
        new_booking = Booking(user_id, self.room_id, start_time, end_time)
        return new_booking