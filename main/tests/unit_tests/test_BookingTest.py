import unittest

from datetime import datetime
import sys
sys.path.insert(0, './')

from main.src.Room import Room
from main.src.Booking import Booking


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

        # Three different room instances with different room numbers
        self.room1 = Room(0, 'Room 1', 'Small', 2, 'Location 1')
        self.room2 = Room(1, 'Room 2', 'Medium', 4, 'Location 2')
        self.room3 = Room(2, 'Room 3', 'Large', 6, 'Location 3')
        
        self.booking = Booking('John Doe', self.room1.room_id, '2022-05-18', '2022-05-18')

        # Two different times, one in evening, one during the day. These are the two different timeframes for the different rates
        # We also have a time period where the rooms cannot be booked, during the night. getPrice() should return -1 in these circumstances
        self.daytime = datetime.strptime('2022-05-18 15:00', '%Y-%m-%d %H:%M')
        self.eveningtime = datetime.strptime('2022-05-18 19:00', '%Y-%m-%d %H:%M')
        self.nighttime = datetime.strptime('2022-05-18 02:00', '%Y-%m-%d %H:%M')
        print(self.booking)
        


    

if __name__ == '__main__':
    unittest.main()
