import sqlite3

conn = sqlite3.connect("academia.db")
cursor = conn.cursor()



cursor.execute(f"DELETE FROM RETURN")
cursor.executemany("""
    INSERT INTO RETURN (return_id, date, student_id, pickup_point_id)
    VALUES (?, ?, ?, ?)
""", [(1, "2023-06-01", 1, 111),
    (2, "2023-06-02", 1, 113),
    ])

cursor.execute(f"DELETE FROM [Contains(RETURN-BOOK)]")
cursor.executemany("""
    INSERT INTO [Contains(RETURN-BOOK)] (return_id, ISBN)
    VALUES (?, ?)
""", [(1, 3182505474745),
    (2, 8293196738353),
    ])

# Commit changes and close the connection
conn.commit()
conn.close()

print("Data has been successfully imported!")