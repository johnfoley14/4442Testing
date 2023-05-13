import datetime
from flask import Flask, request, render_template, redirect
import oracledb
# Replace with your actual Oracle database credentials

#################################################
# MAKE SURE TO CHANGE THESE VALUES TO YOUR OWN! #
#################################################

user = 'SYSTEM'
password = 'root'
port = 1521
service_name = 'XE' # Depending on OS, this could be 'XE' or 'XEPDB1'
conn_string = "localhost:{port}/{service_name}".format(
    port=port, service_name=service_name)
app = Flask(__name__)
data = []
id = []

logged_in = False
logged_in_user = None

#################################################
# Main file for connecting database and routing #
#################################################

#################################################
connection = oracledb.connect(
    user=user, password=password, dsn=conn_string)
cur = connection.cursor()
# Create tables only if they don't alraedy exist
tables = [("ISER.USERS", "USERID VARCHAR2(20) PRIMARY KEY, USERNAME VARCHAR(20), PASSWORD VARCHAR2(20) NOT NULL, EMAIL VARCHAR2(20) NOT NULL, PHONE VARCHAR2(20) NOT NULL"),
          ("ISER.ROOMS", "ROOMID VARCHAR2(20) PRIMARY KEY, ROOMNAME VARCHAR2(20) NOT NULL, ROOMTYPE VARCHAR2(20) NOT NULL, CAPACITY VARCHAR2(20) NOT NULL, LOCATION VARCHAR2(20) NOT NULL"),
          ("ISER.BOOKINGS", "BOOKINGID VARCHAR2(20) PRIMARY KEY, USERID VARCHAR2(20) NOT NULL, ROOMID VARCHAR2(20) NOT NULL, STARTTIME TIMESTAMP NOT NULL, ENDTIME TIMESTAMP NOT NULL, FOREIGN KEY (USERID) REFERENCES ISER.USERS(USERID), FOREIGN KEY (ROOMID) REFERENCES ISER.ROOMS(ROOMID)")]

# loop over the tables and create them if they don't exist
for table in tables:
    # execute the PL/SQL block as a string with parameters
    # This could be done better in the same format as the add rooms loop below but I will leave it as is for now and fix it later if we have time
    plsql_block = """
    declare
      error_code NUMBER;
    begin
      EXECUTE IMMEDIATE '{commandline}';
    exception
      when others then
        error_code := SQLCODE;
        if(error_code = -955)
        then
          dbms_output.put_line('Table {tablename} exists already!'); 
        else
          dbms_output.put_line('Unknown error : '||SQLERRM); 
        end if;
    end;
    """.format(commandline='CREATE TABLE {} ({})'.format(table[0], table[1]), tablename=table[0])
    cur.execute(plsql_block)
    print("Table {} created successfully".format(table[0]))

# Create the rooms if they don't already exist
rooms = [('0', 'Conference Room', 'Meeting', '10', 'East Wing'), 
         ('1', 'AWS Fellows Room', 'Office', '4', 'North Wing'),
         ('2', 'TA Lounge', 'Office', '15', 'North Wing'),
         ('3', 'East Wing Studio', 'Studio', '30', 'East Wing')]

# Loop through all the above-defined rooms and add them to the database if they don't exist
for room in rooms: 
    #cur.execute("DELETE FROM ISER.ROOMS WHERE ROOMID = '{}'".format(room[0])) # Uncomment this line to delete all rooms and re-add them
    
    sql_command = """
    INSERT INTO ISER.ROOMS (ROOMID, ROOMNAME, ROOMTYPE, CAPACITY, LOCATION)
    VALUES (:roomid, :roomname, :roomtype, :capacity, :location)
    """
    params = {'roomid': room[0], 'roomname': room[1], 'roomtype': room[2], 'capacity': room[3], 'location': room[4]}

    try: # Try to execute the SQL command
        cur.execute(sql_command, params)
    except oracledb.DatabaseError as e: # If it fails, print the error
        error_code = e.args[0].code
        if error_code == 955: # If its error 955, the table already exists and should be skipped
            print(f"Room {room[1]} exists already!")
        else:
            print(f"Unknown error: {e}") # If its any other error, print it

    
    print("Room {} created successfully".format(room[1]))

# commit the changes
connection.commit()

# close the cursor and connection
cur.close()
connection.close()
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
    connection = oracledb.connect(
        user=user, password=password, dsn=conn_string)
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
    connection = oracledb.connect(
        user=user, password=password, dsn=conn_string)
    cur = connection.cursor()
    cur.execute('select * from ISER.ROOMS') # Get all the rooms from the database
    data.clear() # Clear the data list before adding new data so that it doesn't keep appending
    for row in cur:
        data.append({"RoomID": row[0], "RoomName": row[1],
                    "RoomType": row[2], "Capacity": row[3], "Location": row[4]})
    # Close the cursor and connection
    cur.close()
    connection.close()
    # Pass the data to the template to display in the HTML table
    return render_template('room.html', data=data)


@app.route('/about_View')
def about():
    return render_template('about.html')


@app.route('/booking_View')
def bookings():
    return render_template('Booking.html')

@app.route('/my_Bookings_View')
def myBookings():
    return render_template('myBookings.html')


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
    con = oracledb.connect(user=user, password=password, dsn=conn_string)
    cur = con.cursor()
    #print("INSERT INTO HR.JOBS(JOB_ID, JOB_TITLE, MIN_SALARY, MAX_SALARY) VALUES (:0, :1, :2,:3)", (id, title,  int(min), int(max)))
    
    cur.execute("INSERT INTO HR.JOBS(JOB_ID, JOB_TITLE, MIN_SALARY, MAX_SALARY) VALUES (:0, :1, :2,:3)", 
                (id, title,  int(min), int(max)))
    con.commit()
    cur.close()
    con.close()
    return render_template('after_submit.html')

@app.route('/login_View', methods=['GET', 'POST'])
def login():
    global logged_in
    global logged_in_user
    if not logged_in:
        error = None
        error2 = None
        if request.method == 'POST' and 'Login' in request.form:
            print("in login")
            if request.form['username'] != 'admin' or request.form['password'] != 'admin':
                error = 'Invalid Credentials. Please try again.'
            else:
                logged_in = True
                logged_in_user = request.form['username']
                return redirect('/')
        elif request.method == 'POST' and 'SignUp' in request.form:
            print("in login")
            if request.form['username'] == 'admin' or request.form['firstname'].lower() == 'admin':
            # HERE WE NEED TO CHECK IF THE USERNAME, EMAIL AND PHONE NUMBER ALREADY EXISTS IN THE DATABASE
                error2 = 'This account already exists'
            if request.form['password'] == 'admin':
            # HERE WE NEED TO CHECK IF THE USERNAME, EMAIL AND PHONE NUMBER ALREADY EXISTS IN THE DATABASE
                error2 = 'This password is already used by admin'
            elif request.form['confpassword'] != request.form['password']:
            # HERE WE CHECK IF PASSWORD IS NOT CONFIRMED. Could also check if passwords are strong enough
                error2 = 'Passwords Dont Match'
                print("Passwords Dont Match")
            else:
            # HERE WE NEED TO INSERT THE USERNAME, PASSWORD, FNAME, LNAME, EMAIL AND PHONE NUMBER IN THE DATABASE
                print("Added user " + request.form['firstname'] + " " + request.form['lastname'] + " with username " + request.form['username'] + "")
                logged_in = True
                logged_in_user = request.form['username']
                return redirect('/')
        
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
    con = oracledb.connect(user=user, password=password, dsn=conn_string)
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
