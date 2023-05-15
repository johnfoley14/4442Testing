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
        # Execute a query to fetch the starttime and endtime from bookings and store into array
        self.cursor.execute("SELECT starttime, endtime FROM bookings")
        bookings = self.cursor.fetchall()

        # Make sure the the starttime is less than, ie before the endtime
        for booking in bookings:
            starttime = booking[0]
            endtime = booking[1]
            self.assertLess(starttime, endtime, "starttime is not before endtime")

    def test_starttime_and_endtime_same_day(self):
        # Execute a query to fetch the starttime and endtime from all the bookings and store them in an array called bookings
        self.cursor.execute("SELECT starttime, endtime FROM bookings")
        bookings = self.cursor.fetchall()

        # For every starttime and endtime in bookings
        for booking in bookings:
            starttime = booking[0]
            endtime = booking[1]
            # Change starttime and endtime to just dates and get rid of the time component
            # From here on we can compare just the dates to ensure a booking starts and finishes on the same day
            start_date = starttime.date()
            end_date = endtime.date()
            self.assertEqual(start_date, end_date, "starttime and endtime are not on the same day")

if __name__ == '__main__':
    unittest.main()
