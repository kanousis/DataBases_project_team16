import tkinter as tk
from PIL import ImageTk, Image
import sqlite3
import io
import datetime

class FinalSelection(tk.Toplevel):
    def __init__(self, master, student_id, total_books, course_id, current_academic_year):
        super().__init__(master)
        self.title("Final Selection")
        self.total_books = total_books
        self.master = master
        self.student_id = student_id
        self.course_id = course_id
        self.curent_academic_year = current_academic_year
        self.geometry("800x300")
        self.configure(bg="#eaddc0")
        self.create_content()

    def create_content(self):
        color = "#eaddc0"

        conn = sqlite3.connect("academia.db")
        cursor = conn.execute("SELECT title FROM COURSE WHERE course_id=?", (self.course_id,))
        course_name = cursor.fetchall()

        main_text = "This are the books you have selected for the course: "+ course_name[0][0]
        top_label = tk.Label(self, text=main_text, font=("Arial", 18, "bold"), bg=color)
        top_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        for i, book in enumerate(self.total_books):
            cursor = conn.execute("SELECT title FROM BOOK WHERE ISBN=?", (book[1],))
            book_name = cursor.fetchall()
            text = f"{book_name[0][0]} | ISBN: {book[1]}"
            book_label = tk.Label(self, text=text, font=("Arial", 12, "bold"), bg=color)
            book_label.grid(row=i+1, column=0, padx=10, pady=10, columnspan=2, sticky="w")

        conn.close()

        self.book_suggestion = tk.StringVar()
        self.book_suggestion.set("Choose ISBN")
        suggestion_label = tk.Label(self, text="Pick your preferred book (optional):", bg=color, font=("Arial", 12, "bold"))
        suggestion_label.grid(row=i+2, column=0, padx=10, pady=10)
        self.book_dropdown = tk.OptionMenu(self, self.book_suggestion, *[book[1] for book in self.total_books])
        self.book_dropdown.grid(row=i+2, column=1, padx=10, pady=10)



        back_button = tk.Button(self, text="Back", command=self.destroy, bg=color)
        back_button.grid(row=i+3, column=0, padx=10, pady=10)


        submit_button = tk.Button(self, text="Submit", command=self.submit_selection, bg=color)
        submit_button.grid(row=i+3, column=1, padx=10, pady=10)


    def destroy(self):
        return super().destroy()

    def submit_selection(self):
        conn = sqlite3.connect("academia.db")
        cursor = conn.cursor()

        cursor.execute("DELETE FROM Participates WHERE course_id=? AND academic_year=?", (self.course_id, self.curent_academic_year))

        for book in self.total_books:
            isbn = book[1]
            if isbn == self.book_suggestion.get():
                cursor.execute("INSERT INTO Participates VALUES(?,?,?,?)", (self.course_id, self.curent_academic_year, isbn, 1))

            else:
                cursor.execute("INSERT INTO Participates VALUES(?,?,?,?)", (self.course_id, self.curent_academic_year, isbn, 0))

        conn.commit()
        conn.close()
        self.destroy()
        self.master.destroy()
        self.master.master.destroy()





        

