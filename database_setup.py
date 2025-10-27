import MySQLdb
from werkzeug.security import generate_password_hash


connection = MySQLdb.connect(
    host="localhost",
    user="adminJanu",
    passwd="LetYourWillBeDoneLord!",
)


cursor = connection.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS faculty_tracker")
cursor.execute("USE faculty_tracker")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        mobile VARCHAR(20),
        email VARCHAR(255) UNIQUE,
        password VARCHAR(255)
    )
""")

# Insert test user
hashed_password = generate_password_hash('jahnavi1205@')
cursor.execute("""
    INSERT IGNORE INTO users (name, mobile, email, password)
    VALUES ('Jahnavi', '1234567890', 'jahnavi.23bce8354@vitapstudent.ac.in', %s)
""", [hashed_password])

connection.commit()
print("✅ Test user created!")


cursor.execute("""
CREATE TABLE IF NOT EXISTS faculty (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    block VARCHAR(10),
    room VARCHAR(10),
    alphabet VARCHAR(5),
    status VARCHAR(20) DEFAULT 'absent'
)
""")
cursor.execute("SELECT * FROM faculty WHERE name='Satyanarayana Moru' AND room='219'")
if cursor.fetchone() is None:
    cursor.execute("""
    INSERT INTO faculty (name, block, room, alphabet, status)
    VALUES 
    ('Satyanarayana Moru', 'CB', '219', 'D', 'present'),
    ('Deepthi Godavarthi', 'CB', '327', 'C', 'absent')
    """)
connection.commit()
print("Database setup complete ✅")
cursor.close()
connection.close()
