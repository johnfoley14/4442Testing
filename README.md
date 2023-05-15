# 4442Testing
Software Testing Project for CS4442

## Setup
Create a postgres server in pgadmin with credentials
```
host: localhost
database: iser
user: postgres
password: root
port: 5432
```
Once this server is running you can launch the flask application by running the main script
Once running you can go to http://127.0.0.1:5000/ to view the application

## Features
### Login
- Users can sign up or login
- Users cannot sign up if their username is taken
- Users cannot sign up if their passwords don't match
- Users cannot login if their account doesn't exist
Tests exist for each of these conditions in the [test_LoginTest](./main/tests/unit_tests/test_LoginTest.py)

### View Rooms
- Users can see all rooms
- If logged in they can create a booking
- Users cannot create a booking if the attendees are higher than the capacity
- Users cannot create a booking if the times overlap, aren't in order or aren't on the same day
Tests exist for each of these conditions in the [test_CapacityTest](./main/tests/unit_tests/test_CapacityTest.py) and [test_NoBookingTimes](./main/tests/unit_tests/test_NoBookingTimes.py)

### View Bookings
- Users can see all active bookings

### View My Bookings
- If logged in, Users can view all their active Bookings
- Users can delete their active bookings

## Percentage Contribution
### Eoghan

### John

### Oisin

