import tkinter as tk
from PIL import ImageTk, Image
import sqlite3
import io

class BookDetailsWindow(tk.Toplevel):
    def __init__(self, master, isbn):
        super().__init__(master, bg='#eaddc0')
        self.title("Book Details")
        self.isbn = isbn
        self.master = master
        self.create_content()

    def create_content(self):
        color1 = '#eaddc0'

        left_frame = tk.Frame(self, bg=color1)
        left_frame.grid(column=0, row=0, columnspan=2)

        right_frame = tk.Frame(self, bg=color1)
        right_frame.grid(column=2, row=0, columnspan=1)

        middle_frame = tk.Frame(self, bg=color1)
        middle_frame.grid(column=0, row=2, columnspan=4)

        # Fetch book details from the database
        conn = sqlite3.connect("academia.db")
        cursor = conn.execute("SELECT ISBN, title, author, cover, pages_number, publisher, credits FROM BOOK WHERE ISBN=?", (self.isbn,))
        data = cursor.fetchall()

        # Display the book cover image
        image_data = io.BytesIO(data[0][3])
        book_cover = Image.open(image_data)
        book_cover = book_cover.resize((200, 250))
        book_cover = ImageTk.PhotoImage(book_cover)

        cover_label = tk.Label(left_frame, image=book_cover, bg=color1)
        cover_label.image = book_cover
        cover_label.grid(column=0, row=0)

        # Display book details in labels
        labels = [
            ("ISBN:", data[0][0]),
            ("Title:", data[0][1]),
            ("Author:", data[0][2]),
            ("Pages:", data[0][4]),
            ("Publisher:", data[0][5]),
            ("Credits:", data[0][6]),
        ]

        for i, (label_text, value) in enumerate(labels):
            label = tk.Label(right_frame, text=label_text, bg=color1, fg='black', font=('Calibri', 12, 'bold'))
            value_label = tk.Label(right_frame, text=value, bg=color1, fg='black', font=('Calibri', 12, 'bold'))
            label.grid(column=0, row=i, sticky='e')
            value_label.grid(column=1, row=i, sticky='w')

        back_btn = tk.Button(middle_frame, text="Back", command=self.destroy, bg=color1)
        back_btn.grid(column=0, row=3, columnspan=2)

        # Average book rating
        cursor = conn.execute("""
            SELECT avg(grade)
            FROM Rates
            WHERE ISBN = ?
        """, (self.isbn,))
        rate = cursor.fetchall()
        
        conn.close()
        if rate[0][0] is None:
            ratingtext = "Rating: No ratings"
        else:
            stars = round(rate[0][0], 1)
            ratingtext = f"Rating: {stars}/10"

        rating_label = tk.Label(self, text=ratingtext, bg=color1, fg='black', font=30, cursor="hand2")
        rating_label.grid(column=1, row=1, columnspan=2)
        rating_label.bind("<Button-1>", lambda event: self.showratings())
        rating_label.bind("<Enter>", lambda event: rating_label.config(bg="#A9D9D9"))
        rating_label.bind("<Leave>", lambda event: rating_label.config(bg=color1))

    def showratings(self):
        self.destroy()
        from read_reviews_page import ReadReviews
        reaviewspg = ReadReviews(self.master, isbn=self.isbn)
        reaviewspg.grid()
