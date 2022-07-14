from flask import Flask, render_template, request, session, redirect, url_for, flash
from multiprocessing import connection
import pymysql

connection = pymysql.connect(host="localhost" , user="root", password="root", database="streamify")
cur = connection.cursor()

app = Flask(__name__)
app.secret_key  = 'mahinthejackfruit'
''''''''''''''''
@app.route('/')
def index():
    return render_template('login.html')

    print("Connected to database")

cur.execute("SELECT * FROM liked_songs")
print("Executed query")
result = cur.fetchall()
print(result)
'''''''''''''''

@app.route('/', methods=['GET', 'POST'])
def login():
    print('in login page')
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']

        print(username, password)
        # Check if account exists using MySQL
        cur.execute('SELECT email, password FROM artist WHERE email= %s AND password = %s UNION SELECT email, password FROM listener WHERE email= %s AND password = %s', (username, password, username, password))
        # Fetch one record and return result
        account = cur.fetchone()

        print(account)
   
    # If account exists in accounts table in out database
        if account:
# Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = username
            print(session['id'])
            # Redirect to home page
            #return 'Logged in successfully!'
            print('it worked')
            cur.execute('SELECT * FROM artist WHERE email = %s', [username])
            account = cur.fetchone()

            if account:
                return render_template('homepage.html')
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
            print('unsuccessful')
    
    return render_template('login.html', msg=msg)

