import datetime
import unittest

from main.src import Booking

class test_Capacity(unittest.Testcase):


    def test_attendee_capacity():
        # Create a booking with valid number of attendees
        # eg: 0, 10, 'Conference Room', 'Meeting', 'East Wing
        # roomID, capacity, roomName, roomType, location
        booking = Booking(roomID=0, capacity=10, roomName = 'Conference Room', roomType = 'Meeting', attendees = 6)
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