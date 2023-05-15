from datetime import datetime
import psycopg2
import sys
sys.path.insert(0, './')

conn = None
host="localhost"
database="postgres"
user="postgres"
password="root"
port = 5432


class Booking:
    def __init__(self, user_id, room_id, start_time, end_time):
        self.user_id = user_id
        self.room_id = room_id
        self.start_time = start_time
        self.end_time = end_time

    
    def createBooking(self, id):
        connection = psycopg2.connect(
                host= host,
                database= database,
                user= user,
                password=password,
                port = port)
        cur = connection.cursor()
        
        cur.execute('select max(bookingid) from bookings')
        id = int(cur.fetchone()[0]) + 1
        cur.execute('insert into bookings (bookingid, roomid, userid, starttime, endtime) values (%s, %s, %s, %s, %s)', (id, self.room_id, self.user_id, self.start_time, self.end_time))
        connection.commit()
        cur.close()
        connection.close()

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
        
    
    def get_all_bookings(self):
        data = []
        connection = psycopg2.connect(
            host= host,
            database= database,
            user= user,
            password=password,
            port = port)
        cur = connection.cursor()
        data.clear()
        cur.execute('select * from bookings')
        for row in cur.fetchall():
            cur.execute('select roomname from rooms where roomid = %s', (row[1],))
            rname = cur.fetchone()[0]
            cur.execute('select username from users where userid = %s', (row[2],))
            uname = cur.fetchone()[0]
            data.append({"bookingid": str(row[0]), "roomname":rname, "username":uname, "starttime": row[3], "endtime": row[4]})
        cur.close()
        connection.close()
        
        return data
        