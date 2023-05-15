import sys 
sys.path.insert(0, './')

from main.src import main
import unittest
from main.src.main import app


class TestLogin(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        

    def test_login_with_wrong_username(self):
        # Test with incorrect username
        self.app.post('/login_View', data=dict(username="incorrect_user_yyyyyyyyyyy", password="correct_password", Login="Login"), follow_redirects=True)
        print(main.error)
        self.assertEqual('User does not exist. Please sign up.', main.error)
    
    def test_login_with_correct_credentials(self):
        # Test with correct credentials
        self.app.post('/login_View', data=dict(username="admin", password="admin", Login="Login"), follow_redirects=True)
        self.assertEqual('Login successful', main.error)

    def test_login_with_incorrect_password(self):# Test with incorrect credentials
        self.app.post('/login_View', data=dict(username="admin", password="dfghjaddahbhadb", Login="Login"), follow_redirects=True)
        # For some reason you have to post twice in 1 of the functions. Dont ask me why. You just do
        self.app.post('/login_View', data=dict(username="admin", password="dfghjaddahbhadb", Login="Login"), follow_redirects=True)
        self.assertEqual('Invalid Credentials. Please try again.', main.error)

if __name__ == '__main__':
    unittest.main()