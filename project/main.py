import datetime
from flask import Flask, request, render_template
import oracledb
# Replace with your actual Oracle database credentials
user = 'SYSTEM'
password = 'root'
port = 1521
service_name = 'XEPDB1'
conn_string = "localhost:{port}/{service_name}".format(
    port=port, service_name=service_name)
app = Flask(__name__)
data = []
id = []

# get Job_Ids from Employee Table
connection = oracledb.connect(
    user=user, password=password, dsn=conn_string)
cur = connection.cursor()
job_id = cur.execute('select JOB_ID from HR.JOBS')
for row in job_id:
    id.append(row[0])
cur.close()
connection.close()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/employee_view', methods=['GET', 'POST'])
def get_data():
    connection = oracledb.connect(
        user=user, password=password, dsn=conn_string)
    cur = connection.cursor()
    cur.execute('select * from HR.Employees')
    for row in cur:
        data.append({"FirstName": row[1], "LastName": row[2],
                    "Email": row[3], "Phone_Number": row[4], "Salary": row[7]})
    # Close the cursor and connection
    cur.close()
    connection.close()
    # Pass the data to the template to display in the HTML table
    return render_template('index.html', data=data, job_id=id)


@app.route('/jobs_view',methods=['GET'])
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
