import sqlite3 
import pandas as pd
import random

csv_file = 'data/ECE_all_Courses.csv' 

courses_df = pd.read_csv(csv_file, delimiter=';', usecols=['course_id', 'semester'])

professor_id = [
    1111111,
    1111112,
    1111113,
    1111114,
    1111115,
    1111116,
    1111117,
    1111118,
    1111119,
    1111120,
    1111121,
    1111122,
    1111123,
    1111124,
    1111125,
    1111126,
    1111127,
    1111128,
    1111129,
    1111130,
    1111131,
    1111132,
    1111133,
    1111134,
    1111135,
    1111136,
    1111137,
    1111138,
    1111139,
    1111140
]

# Database connection
conn = sqlite3.connect("academia.db")
cursor = conn.cursor()

cursor.execute(f"DELETE FROM COURSE_TEACHING")
for i in range(len(courses_df)):
    cursor.execute("""
        INSERT INTO COURSE_TEACHING (course_id, semester, academic_year, professor_id)
        VALUES (?, ?, ?, ?)
    """, (courses_df['course_id'][i], int(courses_df['semester'][i]), "2024-2025", professor_id[random.randint(0, len(professor_id)-1)]))


# Commit changes and close the connection
conn.commit()
conn.close()

print("Data has been successfully imported!")