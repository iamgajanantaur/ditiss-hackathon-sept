from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from datetime import datetime, time, timedelta
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set your secret key here

# MySQL configurations
db_config = {
    'host': '172.18.6.158',
    'user': 'mgr',  # Replace with your MySQL username
    'password': 'manager',  # Replace with your MySQL password
    'database': 'hack'  # Replace with your database name
}


# Helper function to establish MySQL connection
def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection


def calculate_work_time(in_time, out_time):
    # If in_time or out_time are None, raise an error
    if in_time is None or out_time is None:
        raise TypeError("in_time and out_time cannot be None")

    # Handle timedelta to time conversion
    if isinstance(in_time, timedelta):
        in_time = (datetime.min + in_time).time()  # Convert timedelta to time
    elif isinstance(in_time, str):
        try:
            in_time = datetime.strptime(in_time, '%H:%M:%S').time()
        except ValueError:
            in_time = datetime.strptime(in_time, '%H:%M').time()

    if isinstance(out_time, timedelta):
        out_time = (datetime.min + out_time).time()
    elif isinstance(out_time, str):
        try:
            out_time = datetime.strptime(out_time, '%H:%M:%S').time()
        except ValueError:
            out_time = datetime.strptime(out_time, '%H:%M').time()

    # Ensure the in_time and out_time are datetime.time objects
    if isinstance(in_time, time) and isinstance(out_time, time):
        total_time = datetime.combine(datetime.min, out_time) - datetime.combine(datetime.min, in_time)
        return total_time
    else:
        raise TypeError("in_time and out_time must be of type datetime.time or valid string format")



@app.route('/')
def home():
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM hr_tech_data WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['name'] = user['name']
            return redirect(url_for('dashboard'))
        else:
            return "Invalid email or password!"

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        mobile = request.form['mobile']
        email = request.form['email']
        pancard = request.form['pancard']
        intw_type = request.form['intw_type']

        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO hr_tech_data (name, password, mobile, email, pancard, intw_type)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, hashed_password, mobile, email, pancard, intw_type))
            conn.commit()
        except mysql.connector.Error as err:
            return f"Error: {err}"
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('login'))

    return render_template('register.html')



@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return render_template('dashboard.html', name=session['name'])
    return redirect(url_for('login'))



@app.route('/enter_details', methods=['GET', 'POST'])
def enter_details():
    if 'email' not in session:
        return redirect(url_for('home'))

    if request.method == 'POST':

        intw_course = request.form['intw_course']
        intw_date = request.form['intw_date']
        in_time = request.form['in_time']
        out_time = request.form['out_time']

        connection = get_db_connection()
        cursor = connection.cursor()

        query = "SELECT id FROM hr_tech_data WHERE email=%s"
        cursor.execute(query, (session['email'],))
        user = cursor.fetchone()

        if user:
            user_id = session['user_id']
            insert_query = """
                INSERT INTO hr_tech_hours (id, intw_course, intw_date, in_time, out_time) 
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (user_id, intw_course, intw_date, in_time, out_time))
            connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for('dashboard'))
    return render_template('enter_details.html')


@app.route('/show_records')
def show_records():
    if 'user_id' not in session:
        return redirect(url_for('home'))

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Fetch records for the currently logged-in user using user_id
    query = """
        SELECT ht.name, ht.mobile, ht.email, ht.pancard, 
               hh.intw_course, hh.intw_date, hh.in_time, hh.out_time,
               TIMEDIFF(hh.out_time, hh.in_time) AS total_work_time
        FROM hr_tech_data ht
        JOIN hr_tech_hours hh ON ht.id = hh.id
        WHERE ht.id = %s
    """

    # Use user_id from session
    cursor.execute(query, (session['user_id'],))
    records = cursor.fetchall()

    cursor.close()
    connection.close()

    # Render the show_all.html template with the fetched records
    return render_template('show_all.html', records=records)


@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('name', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
