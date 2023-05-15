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



    def test_booking_duration():
        # Create a booking with a duration of 1 hour
        booking1 = Booking(user_id=1, room_id=2, start_time=datetime(2023, 5, 15, 9, 0), end_time=datetime(2023, 5, 15, 10, 0))
        booking1.createBooking(id)
        assert booking1.isAvailable() == True

        # Create a booking with a duration of 3 hours(max = 2)
        booking2 = Booking(user_id=2, room_id=2, start_time=datetime(2023, 5, 15, 10, 0), end_time=datetime(2023, 5, 15, 13, 0))
        booking2.createBooking(id)
        assert booking2.isAvailable() == False

        # Create a booking with a duration of 0 hours
        booking3 = Booking(user_id=3, room_id=2, start_time=datetime(2023, 5, 15, 9, 0), end_time=datetime(2023, 5, 15, 9, 0))
        booking3.createBooking(id)
        assert booking3.isAvailable() == False

        # Create a booking with a negative duration
        booking4 = Booking(user_id=4, room_id=2, start_time=datetime(2023, 5, 15, 10, 0), end_time=datetime(2023, 5, 15, 9, 0))
        booking4.createBooking(id)
        assert booking4.isAvailable() == False


    def test_room_availability():
        # Create a booking for a room
        booking = Booking(user_id=1, room_id=2, start_time=datetime.now(), end_time=datetime.now())
        booking.createBooking(id)
        assert booking.isAvailable() == True

        # Try to create another booking for the same room
        conflicting_booking = Booking(user_id=2, room_id=2, start_time=datetime.now(), end_time=datetime.now())
        conflicting_booking.createBooking(id)
        assert conflicting_booking.isAvailable() == False




if __name__ == '__main__':
    unittest.main()
