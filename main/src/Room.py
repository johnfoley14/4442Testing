import psycopg2
from flask import render_template

import sys
sys.path.insert(0, './')

from main.src.Booking import Booking

conn = None
host = "localhost"
database = "postgres"
user = "postgres"
password = "root"
port = 5432

class Room:

    def __init__(self, room_id, room_name, room_type,  capacity, location):
        self.room_id = room_id
        self.room_name = room_name
        self.room_type = room_type
        self.capacity = capacity
        self.location = location

        
    def get_all_rooms(self):
        connection = psycopg2.connect(host= host, database= database, user= user, password=password, port = port)
        cur = connection.cursor()
        data = []
        
        cur.execute('select * from rooms') # Get all the rooms from the database
        data.clear() # Clear the data list before adding new data so that it doesn't keep appending
        for row in cur:
            data.append({"roomname": row[2],
                "roomtype": row[3], "capacity": row[1], "location": row[4]})
    
        # Close the cursor and connection
        cur.close()
        connection.close()
        
        return data

