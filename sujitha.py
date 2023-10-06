import sqlite3
import datetime

# Create and connect to the database
conn = sqlite3.connect('virtual_classroom.db')
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS classrooms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        subject TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        classroom_id INTEGER,
        FOREIGN KEY(classroom_id) REFERENCES classrooms(id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS assignments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        classroom_id INTEGER,
        description TEXT,
        deadline TEXT,
        FOREIGN KEY(classroom_id) REFERENCES classrooms(id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS submissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        assignment_id INTEGER,
        student_id INTEGER,
        submitted_at TEXT,
        FOREIGN KEY(assignment_id) REFERENCES assignments(id),
        FOREIGN KEY(student_id) REFERENCES students(id)
    )
''')

# Function to add a classroom
def add_classroom(name, subject):
    cursor.execute('INSERT INTO classrooms (name, subject) VALUES (?, ?)', (name, subject))
    conn.commit()

# Function to add a student to a classroom
def add_student(name, classroom_id):
    cursor.execute('INSERT INTO students (name, classroom_id) VALUES (?, ?)', (name, classroom_id))
    conn.commit()

# Function to schedule an assignment for a classroom
def schedule_assignment(classroom_id, description, deadline):
    cursor.execute('INSERT INTO assignments (classroom_id, description, deadline) VALUES (?, ?, ?)',
                   (classroom_id, description, deadline))
    conn.commit()

# Function for a student to submit an assignment
def submit_assignment(assignment_id, student_id):
    submitted_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('INSERT INTO submissions (assignment_id, student_id, submitted_at) VALUES (?, ?, ?)',
                   (assignment_id, student_id, submitted_at))
    conn.commit()

# Main function to handle user input
def main():
    while True:
        print("\nVirtual Classroom Manager")
        print("1. Add Classroom")
        print("2. Add Student")
        print("3. Schedule Assignment")
        print("4. Submit Assignment")
        print("5. Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            name = input("Enter classroom name: ")
            subject = input("Enter subject: ")
            add_classroom(name, subject)
            print("Classroom added successfully!")
        elif choice == "2":
            name = input("Enter student name: ")
            classroom_id = input("Enter classroom ID: ")
            add_student(name, classroom_id)
            print("Student added successfully!")
        elif choice == "3":
            classroom_id = input("Enter classroom ID: ")
            description = input("Enter assignment description: ")
            deadline = input("Enter assignment deadline (YYYY-MM-DD HH:MM:SS): ")
            schedule_assignment(classroom_id, description, deadline)
            print("Assignment scheduled successfully!")
        elif choice == "4":
            assignment_id = input("Enter assignment ID: ")
            student_id = input("Enter student ID: ")
            submit_assignment(assignment_id, student_id)
            print("Assignment submitted successfully!")
        elif choice == "5":
            view_classrooms()
        #elif choice == "6":
           # view_students()
        elif choice == "6":
            view_assignments()
        elif choice == "7":
            view_submissions()
        elif choice == "8":
            print("Exiting the Virtual Classroom Manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the main function
if _name_ == "_main_":
    main()

# Close the database connection
conn.close()