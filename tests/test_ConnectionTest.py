from unittest import TestCase
import oracledb
import sys
import os

main = sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/source/main.py')))

#from main import connection


# from src.source import main

user = 'SYSTEM'
password = 'root'
port = 1521
service_name = 'XE' # Depending on OS, this could be 'XE' or 'XEPDB1'
conn_string = "localhost:{port}/{service_name}".format(
    port=port, service_name=service_name)


import oracledb

class TestConnection(TestCase):
    #This Test will fail if the database is not running. Make sure your docker image is running before running this test. 
    def test_connection(self):
        try:
            conn = oracledb.connect('{user}/{pswd}@localhost:{port}/{service_name}'.format(user=user, pswd=password, port=port, service_name=service_name))
            print("Connected to Oracle database!")
            conn.close()
            print("Disconnected from Oracle database!")
            self.assertTrue(True)
        except oracledb.Error as error:
            print("Failed to connect to Oracle database:", error)
            self.assertTrue(False)
            

        


