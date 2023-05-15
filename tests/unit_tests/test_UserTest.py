from unittest import TestCase
import unittest
from src import User

class UserTest(TestCase):
    def test_getName(self):
        user = User("John")
        self.assertEqual("John", user.getName())
        user.setName("John Doe")
        self.assertEqual("John Doe", user.getName())
    
    def test_createdBooking(self):
        user = User("John Doe")
        self.assertFalse(user.hasBooking())
        user.createBooking()
        self.assertTrue(user.hasBooking())
        
    def test_contactDetails(self):
        user = User("John Doe")
        user.setPhoneNumber("0123456789")
        self.assertEqual("0123456789", user.getPhoneNumber())
    
    def test_Booking(self):
        user = User("John Doe")
        user.createBooking("John Doe", "0123456789", "Monday", "16:00", "17:00", 1, 10)
        self.assertEqual("John Doe", user.getBookingName())

    def test_update_booking(self):
        user = User("John Doe")
        user.createBooking("John Doe", "0123456789", "Monday", "16:00", "17:00", 1, 10)
        user.updateBooking("John Doe", "0123456789", "Tuesday", "17:00", "18:00", 2, 15)
        self.assertEqual("Tuesday", user.getBookingDay())
        self.assertEqual("17:00", user.getBookingStartTime())
        self.assertEqual("18:00", user.getBookingEndTime())
        self.assertEqual(2, user.getBookingRoomNumber())
        self.assertEqual(15, user.getBookingCapacity())

    def test_cancel_booking(self):
        user = User("John Doe")
        user.createBooking("John Doe", "0123456789", "Monday", "16:00", "17:00", 1, 10)
        self.assertTrue(user.hasBooking())
        user.cancelBooking()
        self.assertFalse(user.hasBooking())

    def test_display_booking_details(self):
        user = User("John Doe")
        user.createBooking("John Doe", "0123456789", "Monday", "16:00", "17:00", 1, 10)
        expected_output = ("Name: John Doe\n"
                           "Phone Number: 0123456789\n"
                           "Day: Monday\n"
                           "Start Time: 16:00\n"
                           "End Time: 17:00\n"
                           "Room Number: 1\n"
                           "Capacity: 10\n")
        with unittest.mock.patch('builtins.print') as mock_print:
            user.displayBookingDetails()
            mock_print.assert_called_once_with(expected_output)