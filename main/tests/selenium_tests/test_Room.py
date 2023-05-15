import unittest
from datetime import datetime

from Room import *
from src import Room

class test_Room(unittest.TestCase):

    def setUp(self):
        # Create a Room instance for testing
        self.room = Room(room_id=1, room_name="Test Room", room_type="Conference", capacity=10, location="Test Location")

    def test_bookRoom_available(self):
        # Test booking when the room is available
        user_id = 123
        start_time = datetime(2023, 5, 15, 9, 0)  # Replace with desired start time
        end_time = datetime(2023, 5, 15, 10, 0)  # Replace with desired end time

        booking = self.room.bookRoom(user_id, start_time, end_time)

        # Assert that a booking object is returned
        self.assertIsNotNone(booking)
        # Assert that the booking has the correct user_id and room_id
        self.assertEqual(booking.user_id, user_id)
        self.assertEqual(booking.room_id, self.room.room_id)

    def test_bookRoom_unavailable(self):
        # Test booking when the room is unavailable (not implemented)
        pass

if __name__ == '__main__':
    unittest.main()
