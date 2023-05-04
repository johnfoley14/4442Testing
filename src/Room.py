class Room:
    #room_number = None
    #def __init__(self, room_number, driver):
     #   self.room_number = room_number

    def __init__(self):
        self.is_booked = False

    def book_room(self, is_raining):
        if is_raining:
            self.is_booked = True
            return True
        else:
            return False
