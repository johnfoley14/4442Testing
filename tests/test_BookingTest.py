import unittest

from datetime import datetime

from src.Booking import *
from src.Driver import *
from src.Room import *

class BookingTest(unittest.TestCase):
    booking = None
    room1 = None
    room2 = None
    room3 = None
    daytime = None
    eveningtime = None
    nighttime = None
    
    # Create instances of the driver, room, booking and a date. 
    # Parameters of Booking not known yet, these may be gone back and changed
    # Test different room instances with different times 

    def setUp(self):
        self.driver = Driver()

        # Three different room instances with different room numbers
        # Parameteres for room could be number, priceRateNum and capacity. 
        self.room1 = Room(1,self.driver )
        self.room2 = Room(2, self.driver)
        self.room3 = Room(3, self.driver)
        
        self.booking = Booking('John Doe', 1, self.room1 , self.driver)

        # Two different times, one in evening, one during the day. These are the two different timeframes for the different rates
        # We also have a time period where the rooms cannot be booked, during the night. getPrice() should return -1 in these circumstances
        self.daytime = datetime.strptime('2022-05-18 15:00', '%Y-%m-%d %H:%M')
        self.eveningtime = datetime.strptime('2022-05-18 19:00', '%Y-%m-%d %H:%M')
        self.nighttime = datetime.strptime('2022-05-18 02:00', '%Y-%m-%d %H:%M')
        print(self.booking)
        



    def test_get_price(self):
        self.assertEqual(self.booking.getPrice(self.daytime, self.room1.room_number), 100)
        # self.assertEqual(self.booking.getPrice(self.daytime, self.room2.room_number), 120)
        # self.assertEqual(self.booking.getPrice(self.daytime, self.room3.room_number), 150)
        # self.assertEqual(self.booking.getPrice(self.eveningtime, self.room1.room_number), 60)
        # self.assertEqual(self.booking.getPrice(self.eveningtime, self.room2.room_number), 70)
        # self.assertEqual(self.booking.getPrice(self.eveningtime, self.room3.room_number), 80)
        # self.assertEqual(self.booking.getPrice(self.nighttime, self.room1.room_number), -1)
        # self.assertEqual(self.booking.getPrice(self.nighttime, self.room2.room_number), -1)
        # self.assertEqual(self.booking.getPrice(self.nighttime, self.room3.room_number), -1)

if __name__ == '__main__':
    unittest.main()
