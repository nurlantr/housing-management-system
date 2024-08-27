import psycopg2

# Database connection parameters
dbname = "dormitory_db"
user = "nurlantr"
password = "12345"
host = "localhost"
port = "5432"

def clear_dormitory_data():
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        cur = conn.cursor()

        # Update query to set gender and students columns to NULL
        update_query = "UPDATE dormitory SET gender = NULL, students = NULL"
        cur.execute(update_query)

        # Commit the changes
        conn.commit()
        print("Dormitory data cleared successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the cursor and connection
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

# Execute the function to clear data
clear_dormitory_data()
