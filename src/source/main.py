import datetime
from flask import Flask, request, render_template
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

#################################################
# Main file for connecting database and routing #
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


# commit the changes
connection.commit()

# close the cursor and connection
cur.close()
connection.close()


@app.route('/')
def home():
    return render_template('home.html')


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


@app.route('/rooms_view',methods=['GET'])
def update():
    jobs = []
    connection = oracledb.connect(
        user=user, password=password, dsn=conn_string)
    cur = connection.cursor()
    cur.execute('SELECT JOB_ID, JOB_TITLE, MIN_SALARY, MAX_SALARY FROM HR.JOBS')
    for row in cur:
        jobs.append({"JID": row[0], "JTitle": row[1],
                    "minS": row[2], "maxS": row[3]})
    # Close the cursor and connection
    cur.close()
    connection.close()
    # Pass the data to the template to display in the HTML table
    return render_template('jobs.html', data=jobs)
    #return render_template('about.html')


@app.route('/about_View')
def about():
    return render_template('about.html')


@app.route('/Insert_View')
def insert():
    return render_template('Insertion.html', job_id=id)


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

@app.route('/empty_View')
def empty():
    return render_template('empty.html')

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