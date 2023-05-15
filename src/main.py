import datetime
from flask import Flask, request, render_template, redirect
import psycopg2

app = Flask(__name__)
import sys
sys.path.insert(0, './') # Replace '/path/to/main' with the actual path to your main module

from main.src.Booking import Booking

conn = None
host = "localhost"
database = "postgres"
user = "postgres"
password = "root"
port = 5432
app = Flask(__name__)

logged_in = False
logged_in_user = None
logged_in_user_id = None

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

        entriesBookings = [(1, 0, 1234 ,'2023-05-16 10:00:00', '2023-05-17 12:00:00'),(2, 3, 1234, '2023-05-16 13:00:00', '2023-05-17 15:00:00'), (3, 0, 1235, '2023-05-17 13:00:00', '2023-05-18 15:00:00'),  (4, 1, 1236, '2023-05-18 10:00:00', '2023-05-19 12:00:00')]

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


# This needs to be either removed or add a user page to nav that admin can access
@app.route('/user_view', methods=['GET', 'POST'])
def get_data():
    data = []
    connection = psycopg2.connect(
        host= host,
        database= database,
        user= user,
        password=password,
        port = port)
    cur = connection.cursor()
    cur.execute('select * from ISER.USERS')
    for row in cur:
        data.append({"FirstName": row[1], "LastName": row[2],
                    "Email": row[3], "Phone_Number": row[4], "Salary": row[7]})
    # Close the cursor and connection
    cur.close()
    connection.close()
    # Pass the data to the template to display in the HTML table
    return render_template('index.html', data=data, job_id=id)


# Page for viewing all the rooms in the database
# Available to all users with a button to create a booking for that room
# Need to figure out how to implement that create booking and how to link that with the booking class
@app.route('/room_View',methods=['GET'])
def rooms():
    data = []
    connection = psycopg2.connect(
        host= host,
        database= database,
        user= user,
        password=password,
        port = port)
    cur = connection.cursor()
    cur.execute('select * from rooms') # Get all the rooms from the database
    data.clear() # Clear the data list before adding new data so that it doesn't keep appending
    for row in cur:
        data.append({"roomname": row[2],
                    "roomtype": row[3], "capacity": row[1], "location": row[4]})
    # Close the cursor and connection
    cur.close()
    connection.close()
    # Pass the data to the template to display in the HTML table
    return render_template('room.html', data=data)



@app.route('/booking_View')
def bookings():
    global logged_in
    global logged_in_user_id
    data = []
    connection = psycopg2.connect(
        host= host,
        database= database,
        user= user,
        password=password,
        port = port)
    cur = connection.cursor()
    data.clear()
    cur.execute('select * from bookings')
    for row in cur.fetchall():
        cur.execute('select roomname from rooms where roomid = %s', (row[1],))
        rname = cur.fetchone()[0]
        cur.execute('select username from users where userid = %s', (row[2],))
        uname = cur.fetchone()[0]
        data.append({"bookingid": str(row[0]), "roomname":rname, "username":uname, "starttime": row[3], "endtime": row[4]})
    cur.close()
    connection.close()
    
    return render_template('Booking.html', data=data)

@app.route('/my_Bookings_View')
def myBookings():
    global logged_in
    global logged_in_user_id
    data = []
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
            booking =  Booking(room_id=roomid, user_id=userid, start_time=starttime, end_time=endtime)
            # Add the booking to the database
            
            # We want to move this block into the booking class
            # We can then test this using insert and select commands in the database
            
            # Need to add column for no. of attendees
            cur.execute('select max(bookingid) from bookings')
            id = int(cur.fetchone()[0]) + 1
            cur.execute('insert into bookings (bookingid, roomid, userid, starttime, endtime) values (%s, %s, %s, %s, %s)', (id, booking.room_id, booking.user_id, booking.start_time, booking.end_time))
            connection.commit()
            cur.close()
            connection.close()
            return redirect('/booking_View')
        else:
            return render_template('createBooking.html')

@app.route('/Insertion_data', methods=["GET", "POST"])
def getData():
    fname = request.form["fname"]
    lname = request.form["lname"]
    email = request.form["email"]
    num = request.form["phone"]
    job = request.form["job_id"]
    date = request.form["date"]
    print(request.form)
    Name = fname + " " + lname
    return render_template('data.html', name=Name, Email=email, Number=num, JOB=job, Date=date)

@app.route('/Insert_jobs', methods=["GET", "POST"])
def getjobsData():
    id = request.form["id"]
    title = request.form["title"]
    min = request.form["min"]
    max = request.form["max"]
    con = psycopg2.connect(
        host= host,
        database= database,
        user= user,
        password=password,
        port = port)
    cur = con.cursor()
    #print("INSERT INTO HR.JOBS(JOB_ID, JOB_TITLE, MIN_SALARY, MAX_SALARY) VALUES (:0, :1, :2,:3)", (id, title,  int(min), int(max)))
    
    cur.execute("INSERT INTO HR.JOBS(JOB_ID, JOB_TITLE, MIN_SALARY, MAX_SALARY) VALUES (:0, :1, :2,:3)", 
                (id, title,  int(min), int(max)))
    con.commit()
    cur.close()
    con.close()
    return render_template('after_submit.html')


# Login page that checks if the user is logged in or not
# If the user is logged in, show the logout button
# If the user is not logged in, show the login button and the signup button
@app.route('/login_View', methods=['GET', 'POST'])
def login():
    global logged_in
    global logged_in_user
    global logged_in_user_id
    corr_password = None
    connection = psycopg2.connect(
        host= host,
        database= database,
        user= user,
        password=password,
        port = port)
    cur = connection.cursor()
    if not logged_in:
        error = None
        error2 = None
        if request.method == 'POST' and 'Login' in request.form:
            print("in login")
            try:
                cur.execute("select password from users where username = '{}'".format(request.form['username']))#
                corr_password = cur.fetchone()[0]
                if corr_password != request.form['password']:
                    error = 'Invalid Credentials. Please try again.'
                    print(error)
                else:
                    logged_in = True
                    logged_in_user = request.form['username']
                    cur.execute("select userid from users where username = '{}'".format(logged_in_user))
                    logged_in_user_id = cur.fetchone()[0]
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
                print("INSERT INTO USERS (USERID, USERNAME, PASSWORD, EMAIL, PHONE) VALUES ('{}', '{}', '{}', '{}', '{}')".format(logged_in_user_id, logged_in_user, request.form['password'], request.form['email'], request.form['phone']))
                cur.execute("insert into users (USERID, USERNAME, PASSWORD, EMAIL, PHONE) VALUES ('{}', '{}', '{}', '{}', '{}')".format(logged_in_user_id, logged_in_user, request.form['password'], request.form['email'], request.form['phone']))
                connection.commit()
                return redirect('/')
        
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

@app.route('/insert_jobs_View')
def jobs_view():
    return render_template('Insert_jobs.html')



@app.route("/submit_form", methods=["GET", "POST"])
def submit_form():
    con = psycopg2.connect(
        host= host,
        database= database,
        user= user,
        password=password,
        port = port)
    cur = con.cursor()
    Id = request.form["id"]
    fname = request.form["fname"]
    lname = request.form["lname"]
    email = request.form["email"]
    num = request.form["phone"]
    salary = request.form["salary"]
    comm = request.form["Commission"]
    job = request.form["job_id"]
    date = request.form["date"]
    date_obj = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    # Insert the data into the database
    cur.execute("INSERT INTO HR.Employees (EMPLOYEE_ID,FIRST_NAME, LAST_NAME, EMAIL,PHONE_NUMBER,HIRE_DATE,JOB_ID,SALARY,COMMISSION_PCT,MANAGER_ID,DEPARTMENT_ID) VALUES (:0, :1, :2,:3,:4,:5,:6,:7,:8,:9,:10)", (int(
        Id), fname, lname, email, num, date_obj, job, int(salary), float(comm), None, None))
    return render_template('after_submit.html')


if __name__ == '__main__':
    app.run()
