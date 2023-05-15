from unittest import TestCase
import oracledb

user = 'SYSTEM'
password = 'root'
port = 1521
service_name = 'XE' # Depending on OS, this could be 'XE' or 'XEPDB1'
conn_string = "localhost:{port}/{service_name}".format(
    port=port, service_name=service_name)


#import oracledb

class TestConnection(TestCase):
    #This Test will fail if the database is not running.  
    def test_connection(self):
        try:
            conn = oracledb.connect(user=user, password=password, dsn=conn_string)
            #conn = oracledb.connect('{user}/{pswd}@localhost:{port}/{service_name}'.format(user=user, pswd=password, port=port, service_name=service_name))
            print("Connected to database!")
            conn.close()
            print("Disconnected from database!")
            self.assertTrue(True)
        except oracledb.Error as error:
            print("Failed to connect to database:", error)
            self.assertTrue(False)
            

        


