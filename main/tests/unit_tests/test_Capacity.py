import curses
import datetime
from typing import Self
import unittest

from main.src import Booking
from main.src import Room

class test_Capacity(unittest.Testcase):


    def test_attendee_capacity(self, cur):
        # Create a booking with valid number of attendees
        # eg: 0, 10, 'Conference Room', 'Meeting', 'East Wing
        # roomID, capacity, roomName, roomType, location

        curses.execute('select capacity from rooms where roomid = %s', (Self.room_id,))
        if int(cur.fetchone()[0]) < int(self.attendees):

            return False

        elif self.attendees < 1:

            return False

        else:



        room = Room(roomID=0, capacity=10, roomName = 'Conference Room', roomType = 'Meeting', attendees = 6)
        booking.createBooking(id)

        assert booking.isAvailable() == True

        # Create a booking with 0 attendees
        booking = Booking(roomID=0, capacity=10, roomName = 'Conference Room', roomType = 'Meeting', attendees=0)
        booking.createBooking(id)
        assert booking.isAvailable() == False

        # Create a booking with negative number of attendees
        booking = Booking(roomID=0, capacity=10, roomName = 'Conference Room', roomType = 'Meeting', attendees=-5)
        booking.createBooking(id)
        assert booking.isAvailable() == False

        # Create booking with more than 10 attendees
        booking = Booking(roomID=0, capacity=10, roomName = 'Conference Room', roomType = 'Meeting', attendees=19)
        booking.createBooking(id)
        assert booking.isAvailable() == False