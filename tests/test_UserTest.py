
import unittest
from src.User import User
import sys
sys.path.insert(0, '.')


class test_UserTest(unittest.TestCase):

    def test_register(self):
        user = User("John Doe", "john.doe@example.com", "password123")
        user.register()
        self.assertEqual(user.name, "John Doe")
        self.assertEqual(user.email, "john.doe@example.com")
        self.assertEqual(user.password, "password123")

    def test_login(self):
        user = User("Jane Doe", "jane.doe@example.com", "password456")
        user.login()
        self.assertEqual(user.name, "Jane Doe")
        self.assertEqual(user.email, "jane.doe@example.com")
        self.assertEqual(user.password, "password456")

    def test_book_room(self):
        user = User("Alice", "alice@example.com", "password789")
        room_number = 101
        user.book_room(room_number)
        self.assertEqual(user.name, "Alice")
        self.assertEqual(user.email, "alice@example.com")
        self.assertEqual(user.password, "password789")
        self.assertEqual(user.book_room, room_number)

if __name__ == "__main__":
    unittest.main()
