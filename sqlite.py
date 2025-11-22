import sqlite3

# Connect to SQLite database
connection = sqlite3.connect("text2sql.db")
cursor = connection.cursor()

# 1. CREATE STUDENT TABLE

cursor.execute("""
CREATE TABLE IF NOT EXISTS STUDENT (
    ROLL_NO INTEGER PRIMARY KEY,
    NAME VARCHAR(25),
    CLASS VARCHAR(25),
    SECTION VARCHAR(25),
    MARKS INT
);
""")

cursor.execute("SELECT COUNT(*) FROM STUDENT")
if cursor.fetchone()[0] == 0:
    student_data = [
        (1, 'Venkatesh', 'Data Science', 'A', 90),
        (2, 'Rajan', 'Data Engineering', 'B', 100),
        (3, 'Darius', 'Data Science', 'A', 86),
        (4, 'Vikas', 'Data Analysis', 'A', 50),
        (5, 'Dipesh', 'DEVOPS', 'A', 35),
        (6, 'Ram', 'Cyber Security', 'A', 70),
        (7, 'Krishna', 'Product Management', 'B', 72),
        (8, 'Srujan', 'Software Engineering', 'A', 66),
        (9, 'Devvrat', 'Pharma', 'A', 45),
        (10, 'Bheeshma', 'DEVOPS', 'A', 34)
    ]
    cursor.executemany(
        "INSERT INTO STUDENT (ROLL_NO, NAME, CLASS, SECTION, MARKS) VALUES (?, ?, ?, ?, ?)",
        student_data
    )


# 2. CREATE ADDRESS TABLE

cursor.execute("""
CREATE TABLE IF NOT EXISTS ADDRESS (
    ADDRESS_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    ROLL_NO INTEGER,
    CITY VARCHAR(50),
    STATE VARCHAR(50),
    COUNTRY VARCHAR(50),
    FOREIGN KEY (ROLL_NO) REFERENCES STUDENT(ROLL_NO)
);
""")

cursor.execute("SELECT COUNT(*) FROM ADDRESS")
if cursor.fetchone()[0] == 0:
    address_data = [
        (1, 'Pune', 'Maharashtra', 'India'),
        (2, 'Mumbai', 'Maharashtra', 'India'),
        (3, 'Bangalore', 'Karnataka', 'India'),
        (4, 'Hyderabad', 'Telangana', 'India'),
        (5, 'Delhi', 'Delhi', 'India'),
        (6, 'Chennai', 'Tamil Nadu', 'India'),
        (7, 'Kolkata', 'West Bengal', 'India'),
        (8, 'Ahmedabad', 'Gujarat', 'India'),
        (9, 'Jaipur', 'Rajasthan', 'India'),
        (10, 'Lucknow', 'Uttar Pradesh', 'India')
    ]
    cursor.executemany(
        "INSERT INTO ADDRESS (ROLL_NO, CITY, STATE, COUNTRY) VALUES (?, ?, ?, ?)",
        address_data
    )


# 3. CREATE TEACHER TABLE (unique per subject)

cursor.execute("""
CREATE TABLE IF NOT EXISTS TEACHER (
    TEACHER_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NAME VARCHAR(25),
    SUBJECT VARCHAR(25),
    SALARY INT,
    INTEREST VARCHAR(50)
);
""")

cursor.execute("SELECT COUNT(*) FROM TEACHER")
if cursor.fetchone()[0] == 0:
    teacher_data = [
        ('Neha', 'Data Science', 65000, 'Reading'),
        ('Amit', 'Data Engineering', 60000, 'Cricket'),
        ('Priya', 'Data Analysis', 58000, 'Music'),
        ('Rohit', 'DEVOPS', 55000, 'Gaming'),
        ('Anita', 'Cyber Security', 62000, 'Yoga'),
        ('Sunil', 'Product Management', 60000, 'Reading'),
        ('Kiran', 'Software Engineering', 59000, 'Coding'),
        ('Rahul', 'Pharma', 57000, 'Reading')
    ]
    cursor.executemany(
        "INSERT INTO TEACHER (NAME, SUBJECT, SALARY, INTEREST) VALUES (?, ?, ?, ?)",
        teacher_data
    )

# DISPLAY DATA

print("\n--- STUDENT TABLE ---")
for row in cursor.execute("SELECT * FROM STUDENT"):
    print(row)

print("\n--- ADDRESS TABLE ---")
for row in cursor.execute("SELECT * FROM ADDRESS"):
    print(row)

print("\n--- TEACHER TABLE ---")
for row in cursor.execute("SELECT * FROM TEACHER"):
    print(row)

# Commit and close
connection.commit()
connection.close()

print("\nDatabase setup completed successfully!")
