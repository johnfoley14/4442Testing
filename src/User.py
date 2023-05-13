from src.Booking import *

class User:
    name = None
    bookingExists = False
    phoneNumber = None
    booking = None
    def __init__(self, name):
        self.name = name
        
    def setName(self, name):
        self.name = name
        
    def getName(self):
        return self.name
    
    def createBooking(self, name, phoneNumber, day, startTime, endTime, roomNumber, capacity):
        self.bookingExists = True
        self.booking = Booking(name, phoneNumber, day, startTime, endTime, roomNumber, capacity)
        
    def hasBooking(self):
        return self.booking
    
    def setPhoneNumber(self, number):
        self.phoneNumber = number
    
    def getPhoneNumber(self):
        return self.phoneNumber
    
    def getBookingName(self):
        return self.booking.getName()
    
        