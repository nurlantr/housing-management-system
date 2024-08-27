import psycopg2

# Database connection parameters
dbname = "dormitory_db"
user = "nurlantr"
password = "12345"
host = "localhost"
port = "5432"

# Connect to PostgreSQL
conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
cur = conn.cursor()

# Create the table
create_table_query = """
CREATE TABLE IF NOT EXISTS dormitory (
    block INTEGER,
    room INTEGER,
    gender VARCHAR(10),
    students TEXT
);
"""
cur.execute(create_table_query)

# Insert fixed block and room numbers
blocks_db = [22, 23, 24, 25, 26, 27]
floors_db = range(2, 13)  # Floors from 2 to 12
rooms_per_floor_db = range(1, 29)  # Rooms from 1 to 28

# Prepare the insert query
insert_query = "INSERT INTO dormitory (block, room) VALUES (%s, %s) ON CONFLICT DO NOTHING"

# Populate the table with fixed block and room numbers
for block in blocks_db:
    for floor in floors_db:
        for room in rooms_per_floor_db:
            room_number = int(f"{floor:01}{room:02}")
            cur.execute(insert_query, (block, room_number))

# Commit the changes and close the connection
conn.commit()
cur.close()
conn.close()

print("Table created and populated with fixed block and room numbers.")
