import sqlite3
import pandas as pd
import random
import numpy as np

# Load data
csv_file_1 = 'data/ECE_all_Courses.csv'
csv_file_2 = 'data/Books_final.csv' 

courses_df = pd.read_csv(csv_file_1, delimiter=';', usecols=['course_id'])
books_df = pd.read_csv(csv_file_2, delimiter=',', usecols=['ISBN'])

# Database connection
conn = sqlite3.connect("academia.db")
cursor = conn.cursor()

cursor.execute("DELETE FROM Participates")

for i in range(len(courses_df)):
    num_books = int(np.clip(round(np.random.normal(loc=3, scale=1)), 1, 4))  # Number of books to associate with the course
    shuffled_isbns = books_df.sample(frac=1, random_state=random.randint(0, 100)).reset_index(drop=True)
    selected_isbns = shuffled_isbns['ISBN'][:num_books]  # Select unique ISBNs
    
    # Generate book_suggestion values
    suggestions = [0] * num_books
    suggestions[random.randint(0, num_books - 1)] = random.randint(0,1)  # Ensure maximum one value is 1
    
    for isbn, suggestion in zip(selected_isbns, suggestions):
        cursor.execute("""
            INSERT INTO Participates (course_id, academic_year, ISBN, book_suggestion)
            VALUES (?, ?, ?, ?)
        """, (courses_df['course_id'][i], "2024-2025", isbn, suggestion))

# Commit changes and close the connection
conn.commit()
conn.close()

print("Data has been successfully imported!")

