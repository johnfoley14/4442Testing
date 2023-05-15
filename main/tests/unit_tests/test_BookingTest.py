import unittest

from datetime import datetime
import sys
sys.path.insert(0, './')

from main.src.Room import Room
from main.src.Booking import Booking


class test_BookingTest(unittest.TestCase):

    def test_attendee_capacity():
        # Create a booking with valid number of attendees
        booking = Booking(user_id=1, room_id=2, start_time=datetime.now(), end_time=datetime.now(), attendees = 6)
        booking.createBooking(id)
        assert booking.isAvailable() == True

        # Create a booking with 0 attendees
        booking = Booking(user_id=1, room_id=2, start_time=datetime.now(), end_time=datetime.now(), attendees=0)
        booking.createBooking(id)
        assert booking.isAvailable() == False

        # Create a booking with negative number of attendees
        booking = Booking(user_id=1, room_id=2, start_time=datetime.now(), end_time=datetime.now(), attendees=-5)
        booking.createBooking(id)
        assert booking.isAvailable() == False


    def test_booking_overlap():
        # Create a booking with non-overlapping time
        booking1 = Booking(user_id=1, room_id=2, start_time=datetime(2023, 5, 15, 9, 0), end_time=datetime(2023, 5, 15, 10, 0))
        booking1.createBooking(id)
        assert booking1.isAvailable() == True

        # Create a booking with overlapping time
        booking2 = Booking(user_id=2, room_id=2, start_time=datetime(2023, 5, 15, 9, 30), end_time=datetime(2023, 5, 15, 10, 30))
        booking2.createBooking(id)
        assert booking2.isAvailable() == False


    

if __name__ == '__main__':
    unittest.main()
