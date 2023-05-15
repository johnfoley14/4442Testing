from main.src.Booking import Booking

class Room:

    def __init__(self, room_id, room_name, room_type,  capacity, location):
        self.room_id = room_id
        self.room_name = room_name
        self.room_type = room_type
        self.capacity = capacity
        self.location = location


    def bookRoom(self, user_id, start_time, end_time):
        if self.isAvailable():# Create a booking for this room
            new_booking = Booking(user_id, self.room_id, start_time, end_time)
            return new_booking
<<<<<<< HEAD
        
    def isAvailable(roomID, startTime, endTime):
        connection = psycopg2.connect(host= host, database= database, user= user, password=password, port = port)
        cur = connection.cursor()
        cur.execute("SELECT * FROM BOOKINGS WHERE room_id = %s AND start_time <= %s AND end_time >= %s",
                    (roomID, startTime, endTime))
        conflicting_bookings = cur.fetchall()
        cur.close()
        if len(conflicting_bookings) > 0:
            return False
        else:
            return True
    
=======
>>>>>>> bc6d5593450aa336941d7660286c17ae49f7db15
