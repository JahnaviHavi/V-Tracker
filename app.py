from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL
from flask_cors import CORS
import MySQLdb.cursors
import os
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# ---------- DATABASE CONFIG ----------
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', '')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'faculty_tracker')
app.config['MYSQL_PORT'] = int(os.environ.get('MYSQL_PORT', 3306))

mysql = MySQL(app)

# ---------- HOME ----------
@app.route('/')
def home():
    return render_template('open.html')

# ---------- OTHER HTML PAGES ----------
@app.route('/signinpage')
def signinpage():
    return render_template('signin.html')

@app.route('/signuppage')
def signuppage():
    return render_template('signup.html')

@app.route('/option')
def option():
    return render_template('option.html')

@app.route('/block')
def block():
    return render_template('block.html')

@app.route('/ab1')
def ab1():
    return render_template('ab1.html')

@app.route('/ab2')
def ab2():
    return render_template('ab2.html')

@app.route('/cb')
def cb():
    return render_template('cb.html')

@app.route('/name')
def name():
    return render_template('name.html')

# ---------- SIGNUP ----------
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get('name')
    mobile = data.get('mobile')
    email = data.get('email')
    password = data.get('password')
    
    hashed_password = generate_password_hash(password)
    
    try:
        with mysql.connection.cursor() as cursor:
            # Removed CREATE TABLE - do this once via setup script
            cursor.execute("INSERT INTO users (name, mobile, email, password) VALUES (%s, %s, %s, %s)",
                           (name, mobile, email, hashed_password))
            mysql.connection.commit()
        return jsonify({'message': 'User created successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ---------- SIGNIN ----------
@app.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    try:
        with mysql.connection.cursor(MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("SELECT * FROM users WHERE email = %s", [email])
            user = cursor.fetchone()
        
        if user and check_password_hash(user['password'], password):
            return jsonify({'message': 'Login successful', 'name': user['name']})
        else:
            return jsonify({'error': 'Invalid email or password'}), 401
    except Exception as e:
        return jsonify({'error': 'Database connection error'}), 500

# ---------- FACULTY STATUS CHECK ----------
@app.route('/check_faculty_by_name', methods=['POST'])
def check_faculty_by_name():
    data = request.get_json()
    name = data.get('name')
    
    try:
        with mysql.connection.cursor(MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("SELECT * FROM faculty WHERE LOWER(name) = LOWER(%s)", [name])
            faculty = cursor.fetchone()
        
        if faculty:
            return jsonify({
                'status': faculty['status'],
                'block': faculty['block'],
                'room': faculty['room'],
                'alphabet': faculty['alphabet']
            })
        else:
            return jsonify({'error': 'Faculty not found'}), 404
    except Exception as e:
        return jsonify({'error': 'Database error'}), 500

@app.route('/check_faculty', methods=['POST'])
def check_faculty():
    data = request.get_json()
    block = data.get('block')
    room = data.get('cabin')
    alphabet = data.get('alpha')
    
    try:
        with mysql.connection.cursor(MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("SELECT * FROM faculty WHERE block=%s AND room=%s AND alphabet=%s", 
                           (block, room, alphabet))
            faculty = cursor.fetchone()
        
        if faculty:
            return jsonify({'status': faculty['status'], 'name': faculty['name']})
        else:
            return jsonify({'status': 'absent'})
    except Exception as e:
        return jsonify({'error': 'Database error'}), 500

@app.route('/update_sensor_status_by_location', methods=['POST'])
def update_sensor_status_by_location():
    data = request.get_json()
    block = data.get('block')
    room = data.get('room')
    alphabet = data.get('alphabet')
    status = data.get('status')
    
    try:
        with mysql.connection.cursor() as cursor:
            cursor.execute("""
                UPDATE faculty 
                SET status = %s 
                WHERE block = %s AND room = %s AND alphabet = %s
            """, (status, block, room, alphabet))
            mysql.connection.commit()
        return jsonify({'message': 'Faculty status updated successfully'})
    except Exception as e:
        return jsonify({'error': 'Database error'}), 500

# ---------- RUN APP ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
