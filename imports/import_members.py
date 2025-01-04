import sqlite3
import csv

csv_file = 'data/Students.csv'
conn = sqlite3.connect("academia.db")
cursor = conn.cursor()
cursor.execute(f"DELETE FROM MEMBER")
cursor.execute(f"DELETE FROM STUDENT")

with open(csv_file, 'r') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',')
    for row in reader:
        print(row)
        cursor.execute("""
            INSERT INTO MEMBER (member_id, first_name, last_name, street, number, PC, email, telephone, password)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            int(row["member_id"]),
            row["first_name"].strip(),
            row["last_name"].strip(),
            row["street"].strip(),
            int(row["number"]),
            row["PC"].strip(),
            row["email"].strip(),
            int(row["telephone"]),
            row["password"].strip()
        ))

        cursor.execute("""
            INSERT INTO STUDENT (student_id, current_semester, department, credits)
            VALUES (?, ?, ?, ?)
        """, (
            row["student_id"].strip(),
            int(row["current_semester"]),
            row["department"].strip(),
            float(row["credits"])
        ))

# Commit changes and close the connection
conn.commit()
conn.close()

print("Data has been successfully imported!")



# Database connection
conn = sqlite3.connect("academia.db")
cursor = conn.cursor()

cursor.executemany("""
    INSERT INTO MEMBER (member_id, first_name, last_name, street, number, PC, email, telephone, password)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", [(1111111, "Georgios", "Kokkinos", "Kifisias", 123, "54621", "gkokkinos@gamil.com", 6983718920, "1111"),
    (1111112, "Maria", "Papadopoulou", "Omonias", 45, "54622", "maria.papadopoulou@gmail.com", 6983718921, "1112"),
    (1111113, "Nikos", "Georgiou", "Egnatias", 67, "54623", "nikos.georgiou@gmail.com", 6983718922, "1113"),
    (1111114, "Eleni", "Vasileiou", "Tsimiski", 89, "54624", "eleni.vasileiou@gmail.com", 6983718923, "1114"),
    (1111115, "Kostas", "Nikolaou", "Mitropoleos", 101, "54625", "kostas.nikolaou@gmail.com", 6983718924, "1115"),
    (1111116, "Dimitris", "Ioannou", "Aristotelous", 123, "54626", "dimitris.ioannou@gmail.com", 6983718925, "1116"),
    (1111117, "Giannis", "Papadakis", "Venizelou", 145, "54627", "giannis.papadakis@gmail.com", 6983718926, "1117"),
    (1111118, "Sofia", "Kostopoulou", "Agias Sofias", 167, "54628", "sofia.kostopoulou@gmail.com", 6983718927, "1118"),
    (1111119, "Panagiotis", "Kotsis", "Ethnikis Amynis", 189, "54629", "panagiotis.kotsis@gmail.com", 6983718928, "1119"),
    (1111120, "Vasilis", "Koutroumanos", "Tsimiski", 201, "54630", "vasilis.koutroumanos@gmail.com", 6983718929, "1120"),
    (1111121, "Christina", "Mavridou", "Mitropoleos", 223, "54631", "christina.mavridou@gmail.com", 6983718930, "1121"),
    (1111122, "Petros", "Koufos", "Egnatias", 245, "54632", "petros.koufos@gmail.com", 6983718931, "1122"),
    (1111123, "Anna", "Papageorgiou", "Omonias", 267, "54633", "anna.papageorgiou@gmail.com", 6983718932, "1123"),
    (1111124, "Stavros", "Katsaros", "Aristotelous", 289, "54634", "stavros.katsaros@gmail.com", 6983718933, "1124"),
    (1111125, "Eirini", "Papadimitriou", "Venizelou", 301, "54635", "eirini.papadimitriou@gmail.com", 6983718934, "1125"),
    (1111126, "Alexandros", "Koutroumanos", "Agias Sofias", 323, "54636", "alexandros.koutroumanos@gmail.com", 6983718935, "1126"),
    (1111127, "Maria", "Kotsis", "Ethnikis Amynis", 345, "54637", "maria.kotsis@gmail.com", 6983718936, "1127"),
    (1111128, "Nikos", "Papadopoulos", "Tsimiski", 367, "54638", "nikos.papadopoulos@gmail.com", 6983718937, "1128"),
    (1111129, "Eleni", "Georgiou", "Mitropoleos", 389, "54639", "eleni.georgiou@gmail.com", 6983718938, "1129"),
    (1111130, "Kostas", "Vasileiou", "Egnatias", 401, "54640", "kostas.vasileiou@gmail.com", 6983718939, "1130"),
    (1111131, "Dimitris", "Nikolaou", "Omonias", 423, "54641", "dimitris.nikolaou@gmail.com", 6983718940, "1131"),
    (1111132, "Giannis", "Ioannou", "Aristotelous", 445, "54642", "giannis.ioannou@gmail.com", 6983718941, "1132"),
    (1111133, "Sofia", "Papadakis", "Venizelou", 467, "54643", "sofia.papadakis@gmail.com", 6983718942, "1133"),
    (1111134, "Panagiotis", "Kostopoulou", "Agias Sofias", 489, "54644", "panagiotis.kostopoulou@gmail.com", 6983718943, "1134"),
    (1111135, "Vasilis", "Kotsis", "Ethnikis Amynis", 501, "54645", "vasilis.kotsis@gmail.com", 6983718944, "1135"),
    (1111136, "Christina", "Koutroumanos", "Tsimiski", 523, "54646", "christina.koutroumanos@gmail.com", 6983718945, "1136"),
    (1111137, "Petros", "Mavridou", "Mitropoleos", 545, "54647", "petros.mavridou@gmail.com", 6983718946, "1137"),
    (1111138, "Anna", "Koufos", "Egnatias", 567, "54648", "anna.koufos@gmail.com", 6983718947, "1138"),
    (1111139, "Stavros", "Papageorgiou", "Omonias", 589, "54649", "stavros.papageorgiou@gmail.com", 6983718948, "1139"),
    (1111140, "Eirini", "Katsaros", "Aristotelous", 601, "54650", "eirini.katsaros@gmail.com", 6983718949, "1140")
    
])

cursor.execute(f"DELETE FROM PROFESSOR")
cursor.executemany("""
    INSERT INTO PROFESSOR (professor_id)
    VALUES (?)
""", [(professor_id,) for professor_id in [
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
]])

# Commit changes and close the connection
conn.commit()
conn.close()

print("Data has been successfully imported!")