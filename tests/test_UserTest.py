from unittest import TestCase
from src.User import *

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