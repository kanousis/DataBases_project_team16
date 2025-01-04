import sqlite3
import pandas as pd
import random
import numpy as np


Good_Comments = [
    "Thats a great book!",
    "I really enjoyed this book!",
    "I would recommend this book to anyone!",
    "This book is a must-have!",
    "This book is amazing! I found the solved examples really helpfull!",
    "This book is a masterpiece!",
    "Used this book througthout the semester and it was great!",
    "Used this book for my thesis and it was very helpful!",
    "Used this book througth my studies and it was very helpful!",
    "I would recommend this book to anyone interested in the subject!",
    "This book is a must-have for any student!",
    "Probably the book i enjoyed the most during my studies!"
]


Bad_Comments = [
    "I would not reccomend this book",
    "This book was not very helpful",
    "This book was not very useful",
    "Probably there are better options for this subject",
    "I didn't find this book as usefull as i originally hoped",
    "The luck of examples made it difficult to understand the concepts addressed in this book"
]

# Load data
csv_file_1 = 'data/Students.csv'
csv_file_2 = 'data/Books_final.csv' 

students_df = pd.read_csv(csv_file_1, delimiter=',', usecols=['student_id'])
books_df = pd.read_csv(csv_file_2, delimiter=',', usecols=['ISBN'])

# Database connection
conn = sqlite3.connect("academia.db")
cursor = conn.cursor()

cursor.execute("DELETE FROM Rates")

for i in range(len(students_df)):
    num_books_to_rate = np.random.randint(0,5)
    shuffled_isbns = books_df.sample(frac=1, random_state=random.randint(0, 100)).reset_index(drop=True)
    selected_isbns_to_rate = shuffled_isbns['ISBN'][:num_books_to_rate] 

    ratings=[]
    comments=[]

    for j in range(num_books_to_rate):
        rating = int(np.clip(round(np.random.normal(loc=7, scale=5)), 1, 10))
        if rating > 5:
            Comment = Good_Comments[random.randint(0, len(Good_Comments) - 1)]
        else:
            Comment = Bad_Comments[random.randint(0, len(Bad_Comments) - 1)]
        ratings.append(rating)
        comments.append(Comment)



    for isbn,grade,com in zip(selected_isbns_to_rate, ratings, comments):
        cursor.execute("""
            INSERT INTO Rates (ISBN, student_id, comment, grade)
            VALUES (?, ?, ?, ?)
        """, (isbn, int(students_df['student_id'][i]), com, grade))

# Commit changes and close the connection
conn.commit()
conn.close()

print("Data has been successfully imported!")