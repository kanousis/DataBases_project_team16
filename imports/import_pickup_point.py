import sqlite3
import pandas as pd
import random

conn = sqlite3.connect("academia.db")
cursor = conn.cursor()

cursor.execute(f"DELETE FROM PICKUP_POINT")
cursor.executemany("""
    INSERT INTO PICKUP_POINT (pickup_point_id, name, street, number, PC, telephone, email)
    VALUES (?, ?, ?, ?, ?, ?, ?)
""", [
    (111, "Dianomes GOTSIS", "Ρήγα Φεραίου", 19, "26223", 2610225817, "gotsis@gmail.com"),
    (112, "Library Papadopoulos", "Αγίου Νικολάου", 45, "26222", 2610223456, "papadopoulos@gmail.com"),
    (113, "Library Kotsis", "Μαιζώνος", 67, "26221", 2610227890, "kotsis@gmail.com"),
    (114, "Bookstore Papageorgiou", "Κορίνθου", 89, "26224", 2610221234, "papageorgiou@gmail.com"),
    (115, "Library Alexiou", "Γεροκωστοπούλου", 12, "26225", 2610225678, "alexiou@gmail.com"),
    (116, "Dianomes Dimitriou", "Καραϊσκάκη", 34, "26226", 2610229012, "dimitriou@gmail.com"),
    (117, "Bookstore Nikolakopoulos", "Ερμού", 56, "26227", 2610223457, "nikolakopoulos@gmail.com"),
    (118, "Library Georgiou", "Μαιζώνος", 78, "26228", 2610226789, "georgiou@gmail.com"),
    (119, "Bookstore Konstantinou", "Αγίου Ανδρέου", 90, "26229", 2610220123, "konstantinou@gmail.com"),
    (120, "Bookstore Vasileiou", "Κορίνθου", 23, "26230", 2610223458, "vasileiou@gmail.com")
    
])

# Commit changes and close the connection
conn.commit()
conn.close()

print("Data has been successfully imported!")


csv_file = 'data/Books_final.csv' 

books_df = pd.read_csv(csv_file, delimiter=',', usecols=['ISBN'])


# Database connection
conn = sqlite3.connect("academia.db")
cursor = conn.cursor()

pickup_point_id = [111, 112, 113, 114, 115, 116, 117, 118, 119, 120]

cursor.execute(f"DELETE FROM It_Has")
for i in range(len(books_df)):
    num_pickup_points = random.randint(1, 4)  
    shuffled_pickup_point_id = pickup_point_id[:]
    random.shuffle(shuffled_pickup_point_id)
    selected_pickup_point_id = shuffled_pickup_point_id[:num_pickup_points]  

    for j in selected_pickup_point_id:
        cursor.execute("""
            INSERT INTO It_Has (pickup_point_id, ISBN)
            VALUES (?, ?)
        """, (j, books_df['ISBN'][i].astype(str)))


# Commit changes and close the connection
conn.commit()
conn.close()

print("Data has been successfully imported!")