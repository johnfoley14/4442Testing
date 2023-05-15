from unittest import TestCase
import psycopg2

conn = None
host="localhost"
database="postgres"
user="postgres"
password="root"
port = 5432


class TestConnection(TestCase):
    #This Test will fail if the database is not running. 
    def test_connection(self):
        try:
            conn =psycopg2.connect(
                host= host,
                database= database,
                user= user,
                password=password,
                port = port)
            print("Connected to postgresql database!")
            self.assertTrue(True)
            conn.close()
            print("Disconnected from postgresql database!")
            self.assertTrue(True)
        except psycopg2.Error as error:
            print("Failed to connect to postgresql database:", error)
            self.assertTrue(False)
