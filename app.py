from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS
import MySQLdb.cursors
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)


# MySQL database config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'adminJanu'
app.config['MYSQL_PASSWORD'] = 'LetYourWillBeDoneLord!'
app.config['MYSQL_DB'] = 'faculty_tracker'

mysql = MySQL(app)

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get('name')
    mobile = data.get('mobile')
    email = data.get('email')
    password = data.get('password')
    
    hashed_password = generate_password_hash(password)
    
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                mobile VARCHAR(20),
                email VARCHAR(255) UNIQUE,
                password VARCHAR(255)
            )
        """)
        cursor.execute("INSERT INTO users (name, mobile, email, password) VALUES (%s, %s, %s, %s)",
                       (name, mobile, email, hashed_password))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'User created successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM users WHERE email = %s", [email])
    user = cursor.fetchone()
    cursor.close()
    
    if user and check_password_hash(user['password'], password):
        return jsonify({'message': 'Login successful', 'name': user['name']})
    else:
        return jsonify({'error': 'Invalid email or password'}), 401

@app.route('/check_faculty_by_name', methods=['POST'])
def check_faculty_by_name():
    data = request.get_json()
    name = data.get('name')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM faculty WHERE LOWER(name) = LOWER(%s)", [name])
    faculty = cursor.fetchone()
    cursor.close()
    if faculty:
        return jsonify({
            'status': faculty['status'],
            'block': faculty['block'],
            'room': faculty['room'],
            'alphabet': faculty['alphabet']
        })
    else:
        return jsonify({'error': 'Faculty not found'}), 404

@app.route('/check_faculty', methods=['POST'])
def check_faculty():
    data = request.get_json()
    block = data.get('block')
    room = data.get('cabin')
    alphabet = data.get('alpha')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM faculty WHERE block=%s AND room=%s AND alphabet=%s", 
                   (block, room, alphabet))
    faculty = cursor.fetchone()
    cursor.close()
    if faculty:
        return jsonify({'status': faculty['status'], 'name': faculty['name']})
    else:
        return jsonify({'status': 'absent'})

@app.route('/update_sensor_status_by_location', methods=['POST'])
def update_sensor_status_by_location():
    data = request.get_json()
    block = data.get('block')
    room = data.get('room')
    alphabet = data.get('alphabet')
    status = data.get('status')
    cursor = mysql.connection.cursor()
    cursor.execute("""
        UPDATE faculty 
        SET status = %s 
        WHERE block = %s AND room = %s AND alphabet = %s
    """, (status, block, room, alphabet))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'Faculty status updated successfully'})

if __name__ == '__main__':
    app.run(debug=True)
