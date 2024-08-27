import psycopg2

# Database connection parameters
dbname = "dormitory_db"
user = "nurlantr"
password = "12345"
host = "localhost"
port = "5432"

def add_students_to_dormitory():
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        cur = conn.cursor()

        # List of student entries to add
        students = [
            {'Block': 23, 'Room': 1028,'Id': 21, 'Gender': 'Female', 'Degree' : 'Bachelor', 'Year' : 1},
            {'Block': 24, 'Room': 1111,'Id': 22, 'Gender': 'Female', 'Degree' : 'Bachelor', 'Year' : 2},
            {'Block': 25, 'Room': 1115,'Id': 23, 'Gender': 'Female', 'Degree' : 'Bachelor', 'Year' : 3},
            {'Block': 26, 'Room': 1110,'Id': 18, 'Gender': 'Female', 'Degree' : 'Bachelor', 'Year' : 4},
            {'Block': 27, 'Room': 519,'Id': 24, 'Gender': 'Female', 'Degree' : 'Bachelor', 'Year' : 1},
            {'Block': 23, 'Room': 1007,'Id': 13, 'Gender': 'Male', 'Degree' : 'Masters', 'Year' : 2},
            {'Block': 24, 'Room': 1027,'Id': 25, 'Gender': 'Male', 'Ddegree' : 'Masters', 'Year' : 1},
            {'Block': 25, 'Room': 505,'Id': 26, 'Gender': 'Male', 'Degree' : 'Masters', 'Year' : 1},
            {'Block': 26, 'Room': 415,'Id': 27, 'Gender': 'Male', 'Degree' : 'Masters', 'Year' : 2},
            {'Block': 27, 'Room': 903,'Id': 28, 'Gender': 'Male', 'Degree' : 'Masters', 'Year' : 2}
            # {'block': 23, 'room': 1028, 'gender': 'Female', 'student_id': 21},
            # {'block': 24, 'room': 1111, 'gender': 'Female', 'student_id': 22},
            # {'block': 25, 'room': 1115, 'gender': 'Female', 'student_id': 23},
            # {'block': 26, 'room': 1110, 'gender': 'Female', 'student_id': 18},
            # {'block': 27, 'room': 519, 'gender': 'Female', 'student_id': 24},
            # {'block': 23, 'room': 1007, 'gender': 'Male', 'student_id': 13},
            # {'block': 24, 'room': 1027, 'gender': 'Male', 'student_id': 25},
            # {'block': 25, 'room': 505,'gender': 'Male', 'student_id': 26},
            # {'block': 26, 'room': 415, 'gender': 'Male', 'student_id': 27},
            # {'block': 27, 'room': 903, 'gender': 'Male', 'student_id': 28}
            # {'block': 23, 'room': 202, 'gender': 'Male', 'student_id': 12412},
            # {'block': 24, 'room': 1202, 'gender': 'Female', 'student_id': 12413},
            # {'block': 26, 'room': 616, 'gender': 'Male', 'student_id': 12414}
        ]

        # Update query to set gender and students
        for student in students:
            update_query = """
            UPDATE dormitory 
            SET gender = %s, students = %s
            WHERE block = %s AND room = %s
            """
            cur.execute(update_query, (student['Gender'], student['Id'], student['Block'], student['Room']))

        # Commit the changes
        conn.commit()
        print("New students added to the dormitory successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the cursor and connection
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

# Execute the function to add students
add_students_to_dormitory()
