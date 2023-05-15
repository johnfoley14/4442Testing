import sys
sys.path.insert(0, './')

from main.src.Booking import *

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
    
    def updateBooking(self, day, startTime, endTime, roomNumber, capacity):
        if self.bookingExists:
            self.booking.update(day, startTime, endTime, roomNumber, capacity)
        else:
            print("No booking exists to update.")

    def cancelBooking(self):
        if self.bookingExists:
            self.booking = None
            self.bookingExists = False
        else:
            print("No booking exists to cancel.")
            
    def displayBookingDetails(self):
        if self.bookingExists:
            print(f"Name: {self.booking.getName()}")
            print(f"Phone Number: {self.booking.getPhoneNumber()}")
            print(f"Day: {self.booking.getDay()}")
            print(f"Start Time: {self.booking.getStartTime()}")
            print(f"End Time: {self.booking.getEndTime()}")
            print(f"Room Number: {self.booking.getRoomNumber()}")
            print(f"Capacity: {self.booking.getCapacity()}")
        else:
            print("No booking exists to display.")
