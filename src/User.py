class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def register(self):
        print(f"Registering {self.name} with email {self.email} and password {self.password}")

    def login(self):
        print(f"Logging in as {self.name} with email {self.email} and password {self.password}")

    def book_room(self, room_number):
        print(f"{self.name} has booked room {room_number}")
