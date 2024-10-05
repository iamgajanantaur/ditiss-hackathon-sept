from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from datetime import datetime, time, timedelta
app = Flask(__name__)

# MySQL Database Configuration
db_config = {
    'host': '172.18.6.158',
    'user': 'mgr',
    'password': 'manager',
    'database': 'test'
}


# Helper function to calculate total work time
def calculate_work_time(in_time, out_time):
    # If in_time and out_time are time objects, calculate the difference
    if isinstance(in_time, time) and isinstance(out_time, time):  # Correct reference
        total_time = datetime.combine(datetime.min, out_time) - datetime.combine(datetime.min, in_time)
    # If they are timedelta objects, subtract them directly
    elif isinstance(in_time, timedelta) and isinstance(out_time, timedelta):
        total_time = out_time - in_time
    else:
        raise TypeError("in_time and out_time should be either time or timedelta")

    # Ensure that out_time is after in_time
    if total_time.total_seconds() < 0:
        raise ValueError("Out time cannot be earlier than in time")

    return total_time

# Route for form
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        emp_type = request.form['type']
        pan_card = request.form['pan']
        course = request.form['course']
        date = request.form['date']
        in_time = request.form['in_time']
        out_time = request.form['out_time']

        # Save to MySQL
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = """INSERT INTO employee_data (name, mobile, type, pan, course, date, in_time, out_time)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (name, mobile, emp_type, pan_card, course, date, in_time, out_time))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('fetch_info', name=name))

    return render_template('index.html', date=datetime.now().strftime('%Y-%m-%d'))


@app.route('/fetch', methods=['GET', 'POST'])
def fetch_info():
    name = request.args.get('name')

    if request.method == 'POST':
        name = request.form['name']

    # Open the connection
    conn = mysql.connector.connect(**db_config)

    # Use a buffered cursor to avoid unread result issues
    cursor = conn.cursor(buffered=True, dictionary=True)

    try:
        # Execute the query
        query = "SELECT * FROM employee_data WHERE name = %s"
        cursor.execute(query, (name,))

        # Fetch one row
        result = cursor.fetchone()

    finally:
        # Close the cursor and connection properly
        cursor.close()
        conn.close()

    if result:
        try:
            work_time = calculate_work_time(result['in_time'], result['out_time'])
            result['total_work_time'] = work_time
        except ValueError as e:
            result['error'] = str(e)
    else:
        result = None

    return render_template('fetch.html', result=result)

# Route for fetching all records
@app.route('/fetch_all', methods=['GET'])
def fetch_all():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM employee_data"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    # Calculate total work time for all records
    for result in results:
        try:
            work_time = calculate_work_time(result['in_time'], result['out_time'])
            result['total_work_time'] = work_time
        except ValueError as e:
            result['total_work_time'] = "Error calculating time"

    return render_template('fetch_all.html', results=results)


# Route for deleting all records
@app.route('/delete_all', methods=['POST'])
def delete_all():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    query = "DELETE FROM employee_data"
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('fetch_all'))


# Route for deleting by name
@app.route('/delete_by_name', methods=['POST'])
def delete_by_name():
    delete_name = request.form['delete_name']

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    query = "DELETE FROM employee_data WHERE name = %s"
    cursor.execute(query, (delete_name,))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('fetch_all'))


if __name__ == '__main__':
    app.run(debug=True)
