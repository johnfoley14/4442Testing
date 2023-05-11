import unittest
from src.Room import Room

class test_RoomTest(unittest.TestCase):
    def test_book_room(self):
        room = Room()

        # Test booking room when it's raining
        is_raining = True
        result = room.book_room(is_raining)
        self.assertTrue(result, "The room should be booked when it's raining.")
        self.assertTrue(room.is_booked, "The room should be marked as booked when it's raining.")

        # Test booking room when it's not raining
        room.is_booked = False
        is_raining = False
        result = room.book_room(is_raining)
        self.assertFalse(result, "The room shoudn't be booked when it's not raining.")
        self.assertFalse(room.is_booked, "The room should not be marked as booked when it's not raining.")

if __name__ == '__main__':
    unittest.main()
