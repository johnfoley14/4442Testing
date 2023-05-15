# In this file we want to test that for every room there is only one booking and the times do not overlap
import unittest
import psycopg2
from psycopg2 import sql
from flask import Flask, request, render_template, redirect

class BookingTestCase(unittest.TestCase):

    conn = None
host="localhost"
database="iser"
user="postgres"
password="root"
port = 5432

try:
    conn = psycopg2.connect(
        host= host,
        database= database,
        user= user,
        password=password,
        port = port)

             
except Exception as error:
    print(error) 
    

    def test_no_overlap_bookings_for_room(self):
        with conn.cursor() as cursor:
            # Get all unique roomIDs from the Bookings table
            cursor.execute("SELECT DISTINCT roomID FROM Bookings")
            room_ids = [row[0] for row in cursor.fetchall()]

            for room_id in room_ids:
                # Fetch all bookings for a specific roomID
                cursor.execute(
                    sql.SQL("SELECT startTime, endTime FROM Bookings WHERE roomID = {}")
                    .format(sql.Literal(room_id))
                )
                bookings = cursor.fetchall()

                # Sort bookings by startTime
                sorted_bookings = sorted(bookings, key=lambda x: x[0])

                # Check for overlap
                for i in range(len(sorted_bookings) - 1):
                    current_end_time = sorted_bookings[i][1]
                    next_start_time = sorted_bookings[i + 1][0]
                    self.assertLess(current_end_time, next_start_time,
                                    f"Overlap found for roomID {room_id}.")

if __name__ == '__main__':
    unittest.main()
