import sqlite3
import csv

# File paths
csv_file = 'data/ECE_all_Courses.csv'  # Replace with your actual CSV file path
db_file = 'academia.db'  # Replace with your SQLite database file

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect(db_file)
cursor = conn.cursor()
cursor.execute(f"DELETE FROM COURSE")


# Open the CSV file and insert data into the table
with open(csv_file, 'r') as file:
    csv_reader = csv.DictReader(file, delimiter=';')  # Specify the semicolon delimiter
    for row in csv_reader:
        # Print the row to inspect the data
        print(row)

        # Validate and convert data types
        try:
            id = row['course_id'].strip()  
            title = row['title'].strip()  
            sem = int(row['semester']) 
             

            # Insert data into the SQLite database
            cursor.execute('''
            INSERT INTO COURSE (course_id, title, semester)
            VALUES (?, ?, ?)
            ''', (id, title, sem))

        except ValueError as e:
            print(f"Skipping row due to error: {e} - Row data: {row}")

# Commit the transaction and close the connection
conn.commit()
conn.close()

print("Data inserted successfully.")



