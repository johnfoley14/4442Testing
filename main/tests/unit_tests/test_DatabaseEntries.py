# In this file we want to test that for every room there is only one booking and the times do not overlap
import unittest
import psycopg2
from psycopg2 import sql

class BookingTestCase(unittest.TestCase):    

    def setUp(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="iser",
            user="postgres",
            password="root",
            port=5432
        )
        self.cursor = self.conn.cursor()

    def tearDown(self):
        self.cursor.close()
        self.conn.close()

    def test_no_overlap_bookings_for_room(self):
        try:
            self.cursor.execute("SELECT DISTINCT roomID FROM Bookings")
            room_ids = [row[0] for row in self.cursor.fetchall()]

            for room_id in room_ids:
                # Fetch all bookings for a specific roomID
                self.cursor.execute(
                    sql.SQL("SELECT startTime, endTime FROM Bookings WHERE roomID = {}")
                    .format(sql.Literal(room_id))
                )
                bookings = self.cursor.fetchall()

                # Sort bookings by startTime
                sorted_bookings = sorted(bookings, key=lambda x: x[0])

                # Check for overlap
                for i in range(len(sorted_bookings) - 1):
                    current_end_time = sorted_bookings[i][1]
                    next_start_time = sorted_bookings[i + 1][0]
                    self.assertLess(current_end_time, next_start_time,
                                    f"Overlap found for roomID {room_id}.")
        except Exception as error:
            self.fail(f"An error occurred: {error}")

if __name__ == '__main__':
    unittest.main()
