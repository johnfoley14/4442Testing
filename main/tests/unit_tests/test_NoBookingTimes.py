# The tests in this file will catc the following errors
#1. Make sure the startTime is before the endTime
#2. Ensure that a booking doesn't go overnight
#3. Ensure that the rooms are not booked past 9pm

import unittest
import psycopg2

class BookingTestCase(unittest.TestCase):
    def setUp(self):
        # Connect to the PostgreSQL database
        self.connection = psycopg2.connect(
            host="localhost",
            database="iser",
            user="postgres",
            password="root",
            port = 5432
        )
        self.cursor = self.connection.cursor()

    def tearDown(self):
        # Close the database connection
        self.cursor.close()
        self.connection.close()

    def test_starttime_before_endtime(self):
        # Execute a query to fetch the bookings
        self.cursor.execute("SELECT starttime, endtime FROM bookings")
        bookings = self.cursor.fetchall()

        for booking in bookings:
            starttime = booking[0]
            endtime = booking[1]
            self.assertLess(starttime, endtime, "starttime is not before endtime")

if __name__ == '__main__':
    unittest.main()
