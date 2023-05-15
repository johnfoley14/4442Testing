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

- To run the tests run the command 
```shell
pytest pytest main/tests/unit_tests
```

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

## Coverage Report
![image](https://github.com/johnfoley14/4442Testing/assets/73548984/851abebb-ad1b-4aac-a9d8-4012d479d2f1)
The coverage report can be found at [index.html](htmlcov/index.html)
Due to the nature of our project using a large amount of database calls we couldn't get the statement coverage much higher

## Queries to demonstrate tests fail with invalid entries
--create entry that has endtime before starttime
INSERT INTO public.bookings(
	bookingid, roomid, userid, starttime, endtime)
	VALUES (3, 0, 0, '2023-05-16 10:00:00', '2023-05-16 9:00:00');

--create entry that spans overnight
INSERT INTO public.bookings(
	bookingid, roomid, userid, starttime, endtime)
	VALUES (6, 0, 0, '2023-05-16 10:00:00', '2023-05-17 12:00:00');

--create entry that is too late, past 9pm
INSERT INTO public.bookings(
	bookingid, roomid, userid, starttime, endtime)
	VALUES (7, 0, 0, '2023-05-16 18:00:00', '2023-05-16 21:00:00');

--create two entries for a single room at an overlapping time
INSERT INTO public.bookings(
	bookingid, roomid, userid, starttime, endtime)
	VALUES (8, 0, 0, '2023-05-16 10:00:00', '2023-05-16 9:00:00');

## Percentage Contribution
Our project was done in group sessions using pair programming techniques as well as remote work done using version control on git
### Eoghan
33%
- i made the html and database calls for the webpages
- i made the create and delete bookings options
- i made the login and signup functionality
- i made the tests for login and signup
- i helped make the test_CapacityTest file

### John
33%
- i set up the postgres database
- test cases to ensure booking cannot be beyond a certain hour
- test cases to make sure bookings cannot extemd for multiple days
- test cases to make sure starttime is before endtime
- Sample queries to add data to database in main.py
- test case to ensure one room cannot be booked at the same time twice 

### Oisin
33%
- i made the test_CapacityTest file
- i made the Room file
- i attempted to do selenium testing, but was unsuccessful
- i assisted with designing the test cases we would run
- i contributed to the planning of the tests before we wrote the functions themselves
- i helped make the test_BookingTest file
- i assisted making the database
- i helped make the login page
