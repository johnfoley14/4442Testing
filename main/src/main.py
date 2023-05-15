import datetime
from flask import Flask, request, render_template, redirect, make_response
import psycopg2

import sys
sys.path.insert(0, './') # Replace '/path/to/main' with the actual path to your main module

from main.src.Booking import Booking
from main.src.Room import Room

#from main.src.Booking import Booking

conn = None
host = "localhost"
database = "iser"
user = "postgres"
password = "root"
port = 5432
app = Flask(__name__)

logged_in = False
logged_in_user = None
logged_in_user_id = None
error = None

try:  
    # Note on with clause: if an error occurs inside the withclause, all transactions will rollback, ie not get completed.
    # It commits all transactions itself hence no need for conn.commit() 
    # The with clause also closes the cursor automatically so we dont need to do this anymore. It does not close the connection
    with psycopg2.connect(
        host= host,
        database= database,
        user= user,
        password=password,
        port = port) as conn:

        with conn.cursor() as cur:        
            create_users_tables = '''CREATE TABLE if not exists Users(
                                userID      int primary key,
                                username    varchar(255),
                                password    varchar(255),
                                email      varchar(255),
                                firstName    varchar(255),
                                lastName    varchar(255),
                                phoneNum    varchar(255))'''
            
            create_rooms_tables = '''CREATE TABLE if not exists Rooms(
                                roomID      int primary key,
                                capacity    int,
                                roomName    varchar(255),
                                roomType    varchar(255),
                                location    varchar(255))'''
            
            create_bookings_table = '''CREATE TABLE if not exists Bookings(
                                bookingID      int primary key,
                                roomID    int,
                                userID    int,
                                startTime  timestamp,
                                endTime    timestamp, 
                                FOREIGN KEY (roomID) REFERENCES Rooms (roomID),
                                FOREIGN KEY (userID) REFERENCES Users (userID))'''
            
            #get cursor to execute query/script
            cur.execute(create_rooms_tables)
            cur.execute(create_users_tables)
            cur.execute(create_bookings_table)

#if we fail to connect to the database for some reason, we dont want our program to crash, 
#we just want an error to occur to notify us of this error
except Exception as error:
    print(error)   


if conn is not None:
    print("Connected to the database successfully")
    cur = conn.cursor()
        #create a cursor for the database connection
    
    query_check_empty = "SELECT COUNT(*) FROM Rooms"
    cur.execute(query_check_empty)
    count = cur.fetchone()[0]    
                
    if count == 0:
        queryRooms = '''insert into rooms(roomID, capacity, roomName, roomType, location) values (%s, %s, %s, %s, %s)'''
        entriesRooms = [(0, 10, 'Conference Room', 'Meeting', 'East Wing'), 
                    (1, 4, 'AWS Fellows Room', 'Office', 'North Wing'),
                    (2, 15, 'TA Lounge', 'Office', 'North Wing'),
                    (3, 30, 'East Wing Studio', 'Studio', 'East Wing')]
            
        for record in entriesRooms:
            cur.execute(queryRooms, record)

    query_check_empty = "SELECT COUNT(*) FROM users"
    cur.execute(query_check_empty)
    count = cur.fetchone()[0]    
                
    if count == 0:
        queryUsers = '''insert into users(userID, username, password, email, firstname, lastname, phoneNum) values (%s, %s, %s, %s, %s ,%s, %s)'''
        entriesUsers = [(0, "admin", "admin", "John", "Doe", "admin@email.com", "12345"), (1, "mary", "pwd", "mary@gmail.com", "Mary", "McCarthy", "12345678"), (2, "BigH", "notrophies", "blockhead@gmail.com", "Harry", "Maguire", "1234567")]
    
        for record in entriesUsers:
            print(record)
            cur.execute(queryUsers, record)

    query_check_empty = "SELECT COUNT(*) FROM bookings"
    cur.execute(query_check_empty)
    count = cur.fetchone()[0]    
                
    if count == 0:        
        queryBookings = '''insert into Bookings (bookingid, roomid, userid, starttime, endtime) values (%s, %s, %s, %s, %s)'''

        entriesBookings = [(1, 0, 0 ,'2023-05-16 10:00:00', '2023-05-16 11:00:00'), (2, 3, 1, '2023-05-16 11:00:00', '2023-05-16 12:00:00'), (3, 0, 2, '2023-05-17 13:00:00', '2023-05-17 14:00:00'),  (4, 1, 0, '2023-05-18 15:00:00', '2023-05-18 16:00:00')]


        for record in entriesBookings:
            cur.execute(queryBookings, record)
    
    conn.commit()


if conn is not None:
    conn.commit()
    conn.close()

#################################################


#################################################
#                    ROUTING                    #
#################################################


# Home page
@app.route('/')
def home():
    return render_template('home.html')



# Page for viewing all the rooms in the database
# Available to all users with a button to create a booking for that room
@app.route('/room_View',methods=['GET'])
def rooms():
    room = Room(1,"roomname", "roomtype", 1, "location") # Placeholder room object just to allow us to reference its functions
    data = room.get_all_rooms()
    
    # Pass the data to the template to display in the HTML table
    return render_template('room.html', data=data)



@app.route('/booking_View')
def bookings():
    booking = Booking(1, 1, "2021-05-16", "2021-05-17", 1) # Placeholder booking object just to allow us to reference its functions
    data = booking.get_all_bookings()
    
    return render_template('Booking.html', data=data)

@app.route('/my_Bookings_View', methods=['GET', 'POST'])
def myBookings():
    global logged_in
    global logged_in_user_id
    data = []
    if request.method == 'POST':
        datafromjs = request.form['rowid']
        print(datafromjs)
        try:
            connection = psycopg2.connect(
                host= host,
                database= database,
                user= user,
                password=password,
                port = port)
            cur = connection.cursor()
            cur.execute('delete from bookings where bookingid = %s', (datafromjs,))
            connection.commit()
            cur.close()
            connection.close()
        except:
            print("error")
        return render_template('myBookings.html', data=data)
    else:
        data.clear()
        connection = psycopg2.connect(
            host= host,
            database= database,
            user= user,
            password=password,
            port = port)
        cur = connection.cursor()
        if logged_in == False:
            cur.close()
            connection.close()
            return render_template('noBookings.html')
        else:
            cur.execute('select * from bookings where userid = %s', (logged_in_user_id,))
            for row in cur.fetchall():
                cur.execute('select roomname from rooms where roomid = %s', (row[1],))
                data.append({"bookingid": str(row[0]), "roomname":cur.fetchone()[0], "starttime": row[3], "endtime": row[4]})
            cur.close()
            connection.close()
            return render_template('myBookings.html', data=data)


@app.route('/submit_create_booking', methods=['GET', 'POST'])
def create_booking():
    # Here we want to create an instance of the booking class and fill it with the data from the form
    # Then we want to add that instance to the database
    # Then we want to redirect to the bookings page
    global logged_in
    global logged_in_user_id
    if logged_in == False:
        return render_template('noBookings.html') # Change the text to say you need to login to create a booking
    else:
        if request.method == 'POST':
            # Get the data from the form and create a booking object
            connection = psycopg2.connect(
                host= host,
                database= database,
                user= user,
                password=password,
                port = port)
            cur = connection.cursor()
            roomname = request.form['name_in']
            userid = logged_in_user_id
            attendees = request.form['atts_in']
            starttime = request.form['stime_in']
            endtime = request.form['etime_in']
            cur.execute('select roomid from rooms where roomname = %s', (roomname,))
            roomid = cur.fetchone()[0]
            booking =  Booking(room_id=roomid, user_id=userid, start_time=starttime, end_time=endtime, attendees=attendees)
            # Add the booking to the database
            
            cur.execute('select max(bookingid) from bookings')
            id = int(cur.fetchone()[0]) + 1
            if booking.createBooking(id):
                connection.commit()
                cur.close()
                connection.close()
                return redirect('/booking_View')
            else:
                cur.close()
                connection.close()
                return redirect('/room_View')
            
        else:
            return render_template('myBookings.html')


# Login page that checks if the user is logged in or not
# If the user is logged in, show the logout button
# If the user is not logged in, show the login button and the signup button
@app.route('/login_View', methods=['GET', 'POST'])
def login():
    global logged_in
    global logged_in_user
    global logged_in_user_id
    global error
    corr_password = None
    connection = psycopg2.connect(
        host= host,
        database= database,
        user= user,
        password=password,
        port = port)
    cur = connection.cursor()
    if not logged_in:
        error2 = None
        if request.method == 'POST' and 'Login' in request.form:
            
            print("in login")
            try:
                cur.execute("select password from users where username = '{}'".format(request.form['username']))
                corr_password = cur.fetchone()[0]
                if corr_password != request.form['password']:
                    error = "Invalid Credentials. Please try again."
                    print(error)
                else:
                    logged_in = True
                    logged_in_user = request.form['username']
                    cur.execute("select userid from users where username = '{}'".format(logged_in_user))
                    logged_in_user_id = cur.fetchone()[0]
                    error = "Login successful"
                    return redirect('/')
            except:
                error = 'User does not exist. Please sign up.'
                print(error)
            
            
        elif request.method == 'POST' and 'SignUp' in request.form:
            print("in login")
            cur.execute("select username, password from users")
            for row in cur:
                if row[0] == request.form['username']:
            # HERE WE NEED TO CHECK IF THE USERNAME, EMAIL AND PHONE NUMBER ALREADY EXISTS IN THE DATABASE
                    error2 = 'This account already exists'
                    return render_template('login.html',error=error, error2=error2)
                if row[1] == request.form['password']:
            # HERE WE NEED TO CHECK IF THE USERNAME, EMAIL AND PHONE NUMBER ALREADY EXISTS IN THE DATABASE
                    error2 = 'This password is already used by {}'.format(row[0])
                    return render_template('login.html',error=error, error2=error2)
            if request.form['confpassword'] != request.form['password']:
            # HERE WE CHECK IF PASSWORD IS NOT CONFIRMED. Could also check if passwords are strong enough
                error2 = 'Passwords Dont Match'
                print("Passwords Dont Match")
            else:
            # HERE WE NEED TO INSERT THE USERNAME, PASSWORD, FNAME, LNAME, EMAIL AND PHONE NUMBER IN THE DATABASE
                print("Added user " + request.form['firstname'] + " " + request.form['lastname'] + " with username " + request.form['username'] + "")
                logged_in = True
                logged_in_user = request.form['username']
                cur.execute("SELECT MAX(userid) FROM users")
                logged_in_user_id = int(cur.fetchone()[0]) +  1 
                print(logged_in_user_id)
                print("INSERT INTO USERS (USERID, USERNAME, PASSWORD, EMAIL, PHONENUM) VALUES ('{}', '{}', '{}', '{}', '{}')".format(logged_in_user_id, logged_in_user, request.form['password'], request.form['email'], request.form['phone']))
                cur.execute("insert into users (USERID, USERNAME, PASSWORD, EMAIL, PHONENUM) VALUES ('{}', '{}', '{}', '{}', '{}')".format(logged_in_user_id, logged_in_user, request.form['password'], request.form['email'], request.form['phone']))
                connection.commit()
                return redirect('/')
        
        print(error)
        cur.close()
        connection.close()
        return render_template('login.html',error=error, error2=error2)
    else:
        error = None
        if request.method == 'POST':
            #if request.form['Log out'] == 'Logout':
            logged_in = False
            logged_in_user = None
            return redirect('/')
            # else:
            #     error = 'Invalid Credentials. Please try again.'
        return render_template('logged_in.html',user=logged_in_user)

if __name__ == '__main__':
    app.run()
