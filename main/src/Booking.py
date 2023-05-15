from datetime import datetime
import psycopg2
import os

conn = None
host="localhost"
database="iser"
user="postgres"
password="root"
port = 5432


class Booking:
    def __init__(self, user_id, room_id, start_time, end_time):
        self.user_id = user_id
        self.room_id = room_id
        self.start_time = start_time
        self.end_time = end_time

    def getPrice(self):
        # Calculate the price based on the room rate and duration of booking
        duration = self.end_time - self.start_time
        hours = duration.total_seconds() / 3600
        return self.room.rate * hours

    def isAvailable(self):
        connection = psycopg2.connect(host= host, database= database, user= user, password=password, port = port)
        # Check if there is a conflicting booking for this room and time
        cur = connection.cursor()
        cur.execute("SELECT * FROM BOOKINGS WHERE room_id = %s AND start_time <= %s AND end_time >= %s",
                    (self.room_id, self.end_time, self.start_time))
        conflicting_bookings = cur.fetchall()
        cur.close()
        if len(conflicting_bookings) > 0:
            return False
        else:
            return True
        
    def bookRoom(self):
        connection = psycopg2.connect(host= host, database= database, user= user, password=password, port = port)
        # Check if there is a conflicting booking for this room and time
        cur = connection.cursor()
        cur.execute("SELECT * FROM BOOKINGS WHERE room_id = %s AND start_time <= %s AND end_time >= %s",
                    (self.room_id, self.end_time, self.start_time))
        
    # def isAvailable(self):
    #     connection = psycopg2.connect(user=user, password=password, dsn=conn_string)
    #     # Check if there is a conflicting booking for this room and time
    #     cur = connection.cursor()
    #     cur.execute("SELECT * FROM BOOKINGS WHERE room_id = %s AND start_time <= %s AND end_time >= %s",
    #                 (self.room_id, self.end_time, self.start_time))
    #     conflicting_bookings = cur.fetchall()
    #     cur.close()
    #     if len(conflicting_bookings) > 0:
    #         return False
    #     else:
    #         return True