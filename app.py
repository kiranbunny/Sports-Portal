from flask import Flask, flash, render_template, request, redirect, url_for, jsonify, session
import mysql.connector
import logging,sys
from recovery import train_linear_regression
from datetime import timedelta
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)
app.secret_key= '123'

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Database connection configuration
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sairishik2019@",
    database="rishik"
)

cursor = mydb.cursor()

@app.route('/')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    if request.method == 'POST':
        # Check if the logout button was clicked
        if request.form.get('logout') == 'logout':
            session.clear()  # Clear the session data
            return redirect('/login')  # Redirect to the login page

        # Check if the signup button was clicked
        signup_value = request.form.get('signup')
        if signup_value == 'signup':
            return redirect(url_for('signup'))

        # Proceed with login process
        username = request.form['username']
        password = request.form['password']
        session['username'] = username
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM user WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        if user:
            # User exists, redirect to the appropriate page
            if username == "admin@gmail.com":
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('home'))
        else:
            # User doesn't exist or incorrect password, redirect back to login page
            return redirect(url_for('login'))

@app.route('/logout1')
def logout():
    # Clear the session or perform any other logout logic
    # For example:
    # session.clear()
    # Redirect the user to the login page
    return redirect(url_for('login'))

@app.route('/add_coaching_center1', methods=['GET','POST'])
def add_coaching_center1():
    return render_template('coaching.html')

@app.route('/view_coaching_centers', methods=['GET'])
def view_coaching_centers():
    
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM coaching_centers")
    coaching_centers = cursor.fetchall()
    cursor.close()
    
    
    return render_template('coachingadmin.html', coaching_centers=coaching_centers)
@app.route('/delete_coaching_center/<int:center_id>', methods=['POST'])
def delete_coaching_center(center_id):
    if request.method == 'POST':
        cursor = mydb.cursor()
        # Delete the coaching center from the database
        cursor.execute("DELETE FROM coaching_centers WHERE id = %s", (center_id,))
        mydb.commit()
        cursor.close()
        return redirect(url_for('view_coaching_centers'))  # Redirect to the coaching centers page
    else:
        return "Method Not Allowed"

@app.route('/add_coaching_center', methods=['GET', 'POST'])
def add_coaching_center():
    # Check if the user is logged in and is an administrator
    # if not is_admin():
    #     # If not an admin, redirect to an appropriate page or show an error message
    #     return "You are not authorized to access this page."

    if request.method == 'POST':
        center_name = request.form['center_name']
        game = request.form['game']
        contact_number = request.form['contact_number']
        maps_link = request.form['maps_link']
        state = request.form['inputState']
        district = request.form['inputDistrict']
        
        # Handle file upload
        if 'photo' in request.files:
            photo = request.files['photo']
            if photo.filename != '':
                # Save photo to a directory
                photo_filename = secure_filename(photo.filename)
                photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))
            else:
                photo_filename = ''  # No photo uploaded
        
        # Insert data into the database
        cursor = mydb.cursor()
        cursor.execute("INSERT INTO coaching_centers (center_name, game, contact_number, maps_link,photo_filename, state, district) VALUES (%s, %s, %s, %s,%s, %s, %s)", (center_name, game, contact_number, maps_link,photo_filename, state, district))
        mydb.commit()
        cursor.close()
        
        return redirect(url_for('add_coaching_center1'))
    else:
        # Render the form for adding coaching centers
        return render_template('add_coaching_center.html')




@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method=='POST':
        signup_value = request.form.get('signup')
        print(signup_value)
        username = request.form['username']
        password = request.form['password']
        session['username'] = username
        
        if signup_value == 'signup':
            print("Successfully Signed Up")
            # Insert new user into database
            cursor = mydb.cursor()
            cursor.execute("INSERT INTO user (username, password) VALUES (%s, %s)", (username, password))
            mydb.commit()

            return redirect(url_for('login'))
    return render_template('signup.html')
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    return render_template('admin.html')



@app.route('/home', methods=['GET', 'POST'])
def home():
    print("entered home")
    sys.stdout.flush()
    if request.method == 'POST':
        print("enetered post method in home")
        sel = request.form.get('selection')
        print("selection1")
        if sel=='selection':
            print("selection1")
            return redirect(url_for('selection'))
        lgin = request.form.get('loginl')
        if lgin=='loginl':
            print("lgout")
            return redirect(url_for('login'))
        rec=request.form.get('recovery')
        if rec=='recovery':
            return redirect(url_for('recovery'))
        
        coach=request.form.get('coaching')
        if coach=='coaching':
            return redirect(url_for('coaching'))
        
        eve=request.form.get('eventcal')
        if coach=='eventcal':
            return redirect(url_for('eventcal'))
        

    return render_template('home.html')
@app.route('/selection', methods=['POST'])
def selection():
    return render_template('selection.html')
@app.route('/recovery', methods=['GET', 'POST'])
def recovery():
    return render_template('recovery.html')

@app.route('/coaching', methods=['GET', 'POST'])
def coaching():
    if request.method == 'POST':
        # Handle form submission if needed
        pass

    # Query the database to fetch all coaching center details
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM coaching_centers")
    coaching_centers = cursor.fetchall()
    print(coaching_centers)
    cursor.close()
    return render_template('coachingdat.html', coaching_centers=coaching_centers)

@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        print("entered post")
        # Get the form data
        eventName = request.form['eventTitle']
        eventDate = request.form['eventDate']
        startTime = request.form['eventStartTime']
        endTime = request.form['eventEndTime']
        eventDescription = request.form['eventDescription']
        cursor = mydb.cursor()

        # Insert the data into the database
        cursor.execute("INSERT INTO events (eventName, eventDate, startTime, endTime, eventDescription) VALUES (%s, %s, %s, %s, %s)", (eventName, eventDate, startTime, endTime, eventDescription))

        # Commit the changes
        mydb.commit()
    return render_template('admin.html')




@app.route('/login22', methods=['GET', 'POST'])
def login22():
    return render_template('login.html')
@app.route('/submit_data', methods=['GET', 'POST'])
def predit():
    result=0
    if request.method=='POST':
        data=request.form
        print(data)
        calorie = data['calorie']
        l=[]
        l.append(int(data['calorie']))
        l.append(int(data['age']))
        l.append(int(data['weight']))
        l.append(int(data['injury']))
        l.append(int(data['gender']))
        l.append(int(data['type']))
        print(l)
        # cursor = mydb.cursor()
        # cursor.execute("select * from injurytable")
        # dataset=cursor.fetchall()
        # mydb.commit()
        result = train_linear_regression("newinjury.csv", "Recovery_Period", new_data_point=l)
        print(result)
        return render_template('recovery.html',result=result)
    return render_template('recovery.html',result=result)

@app.route('/eventcalendar')
def user_events():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM events ORDER BY eventDate asc")
    events = cursor.fetchall()
    event_list = []
    for event in events:
        event_dict = {
            'id': event[0],
            'eventDate': str(event[1]),  # Convert timedelta to string
            'startTime': str(event[2]),   # Convert timedelta to string
            'endTime': str(event[3]),    # Convert time to string
            'eventName': event[4],
            'eventDescription': event[5]
        }
        event_list.append(event_dict)
    return render_template('events.html', events=event_list)

@app.route('/adminviews', methods=['GET', 'POST'])
def admin_events():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM events ORDER BY eventDate asc")
    events = cursor.fetchall()
    event_list = []
    for event in events:
        event_dict = {
            'id': event[0],
            'eventDate': str(event[1]),  # Convert timedelta to string
            'startTime': str(event[2]),   # Convert timedelta to string
            'endTime': str(event[3]),    # Convert time to string
            'eventName': event[4],
            'eventDescription': event[5]
        }
        event_list.append(event_dict)
        print(event_list)
    return render_template('admin.html', events=event_list)
    
@app.route('/adminviews/delete_event/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    try:
        cursor = mydb.cursor()
        print(event_id)
        cursor.execute("DELETE FROM events WHERE eventId = %s", (event_id,))
        mydb.commit()
        return jsonify({'message': 'Event deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/register')
def register():
    return render_template('form.html')




@app.route('/register_event/<int:event_id>', methods=['POST'])
def register_event(event_id):
    if 'username' in session:
        username = session['username']
        print("Username from session:", username)
        print(event_id)
        try:
            cursor = mydb.cursor()
            # Check if the user is already registered for the event
            cursor.execute("SELECT * FROM registrations WHERE username = %s AND event_id = %s", (username, event_id))
            registration_exists = cursor.fetchone()
            if registration_exists:
                flash('You are already registered for this event!', 'warning')
            else:
                # Fetch game and description associated with the event_id
                cursor.execute("SELECT eventName, eventDescription FROM events WHERE eventId = %s", (event_id,))
                event_data = cursor.fetchone()
                if event_data:
                    game = event_data[0]
                    description = event_data[1]
                    # Insert registration data into the registrations table
                    cursor.execute("INSERT INTO registrations (username, event_id, game, description) VALUES (%s, %s, %s, %s)",
                                   (username, event_id, game, description))
                    mydb.commit()  # Commit the transaction
                    flash('Event registered successfully!', 'success')
                else:
                    flash('Event not found!', 'error')
        except mysql.connector.Error as err:
            # Handle any database errors
            flash(f"Database error: {err}", 'error')
        finally:
            cursor.close()  # Close the cursor
    else:
        flash('Please login to register for events.', 'error')
    return redirect(url_for('user_events'))

####
@app.route('/unregister_event/<int:event_id>', methods=['POST'])
def unregister_event(event_id):
    if 'username' in session:
        username = session['username']
        print(username)
        print(event_id)
        try:
            cursor = mydb.cursor()
            # Delete the registration record for the logged-in user and the specific event
            cursor.execute("DELETE FROM registrations WHERE username = %s AND event_id = %s", (username, event_id))
            mydb.commit()  # Commit the transaction
            flash('Successfully unregistered from the event!', 'success')
        except mysql.connector.Error as err:
            # Handle any database errors
            flash(f"Database error: {err}", 'error')
        finally:
            cursor.close()  # Close the cursor
    else:
        flash('Please login to unregister from events.', 'error')
    return redirect(url_for('show_registered_events'))





####
@app.route('/Show_Registered_Events', methods=['GET','POST'])
def show_registered_events():
    if 'username' in session:
        username = session['username']
        try:
            cursor = mydb.cursor()
            # Fetch registered events for the logged-in user
            cursor.execute("SELECT game, description,event_id FROM registrations WHERE username = %s", (username,))
            registered_events = cursor.fetchall()
            print(registered_events)
            reglist=[]
            for reg in registered_events:
                reg_dict={
                    'name':str(reg[0]),
                    'desc':str(reg[1]),
                    'event_id':str(reg[2])
                }
                reglist.append(reg_dict)
                print(reglist)
            # Close cursor
            cursor.close()
            return render_template('registered_events.html', registered_events=reglist)
        except mysql.connector.Error as err:
            flash(f"Database error: {err}", 'error')
    else:
        flash('Please login to view registered events.', 'error')
        return redirect(url_for('login'))





@app.route('/eventcal', methods=['GET','POST'])
def add_event():
    if request.method == 'POST':
        try:
            print("DATABASE EVENT")
            # Extract event data from request
            event_data = request.json
            event_date = event_data.get('event_date')
            event_name = event_data.get('event_name')
            event_time_from = event_data.get('event_time_from')
            event_time_to = event_data.get('event_time_to')

            print("Event date",event_date)
            print(event_name)
            print(event_time_from)
            print(event_time_to)

            # Insert event into database
            cursor = mydb.cursor()
            print("Connection Successful")
            cursor.execute("INSERT INTO events (event_date, event_name, event_time_from, event_time_to) VALUES (%s, %s, %s, %s)",
                           (event_date, event_name, event_time_from, event_time_to))
            mydb.commit()
            print("Data Saved")
            cursor.close()
            return jsonify({"success": True}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return render_template('event.html')

# Configure Flask logger to output to terminal
app.logger.setLevel(logging.DEBUG)

@app.route('/')
def index():
    app.logger.debug('This is a debug message')
    app.logger.info('This is an info message')
    app.logger.warning('This is a warning message')
    app.logger.error('This is an error message')
    app.logger.critical('This is a critical message')
    return 'Check terminal for log messages'
if __name__ == '__main__':
    app.run(debug=True)