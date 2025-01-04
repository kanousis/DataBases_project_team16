import sqlite3
import csv
import random
import os

def read_image(file_path):
    """Read image file and return binary data."""
    try:
        with open(file_path, 'rb') as file:
            return file.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None


def read_file(file_path):
    """Read a file (image or PDF) and return binary data."""
    try:
        with open(file_path, 'rb') as file:
            return {
                "data": file.read(),
                "type": os.path.splitext(file_path)[1].lower()  # e.g., '.pdf' or '.jpg'
            }
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return {"data": None, "type": None}


# Database connection
conn = sqlite3.connect("academia.db")
cursor = conn.cursor()

# Read CSV and insert data
cursor.execute(f"DELETE FROM BOOK")

with open("data/Books_final.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',')
    for row in reader:
        print(row)
        cover = read_image("data/cover_toc/%s" % row["cover"].strip())
        contents = read_image("data/cover_toc/%s" % row["contents"].strip())
        cursor.execute("""
            INSERT INTO BOOK (ISBN, title, author, pages_number, publisher, contents, cover, credits, average_grade)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row["ISBN"].strip(),
            row["title"].strip(),
            row["author"].strip(),
            int(row["pages_number"]),
            row["publisher"].strip(),
            contents,
            cover,
            round(random.uniform(2, 20), 2),
            None
        ))

# Commit changes and close the connection
conn.commit()
conn.close()

print("Data has been successfully imported!")
