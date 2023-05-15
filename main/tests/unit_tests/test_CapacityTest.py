import unittest

import sys
sys.path.insert(0, './')

from main.src.Booking import Booking

class CapacityTest(unittest.TestCase):
    def test_capTooSmall(self):
        booking = Booking(0, 0, "2022-01-01 12:00:00", "2022-01-01 13:00:00", -1)
        print(booking.createBooking(15))
        self.assertFalse(booking.createBooking(15))
    
    def test_capTooBig(self):
        booking = Booking(0, 0, "2022-01-01 12:00:00", "2022-01-01 13:00:00", 100)
        self.assertFalse(booking.createBooking(15))
    
    def test_capJustRight(self):
        booking = Booking(0, 0, "2022-01-01 12:00:00", "2022-01-01 13:00:00", 2)
        self.assertTrue(booking.createBooking(15))