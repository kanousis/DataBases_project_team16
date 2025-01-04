import tkinter as tk
import sqlite3

class ReadReviews(tk.Toplevel):
    def __init__(self, master, isbn, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.isbn = isbn
        self.configure(bg='#eaddc0')
        self.create_content()

    def create_content(self):
        conn = sqlite3.connect("academia.db")
        cursor = conn.cursor()

        # Fetch reviews from the Rates table
        cursor.execute("""
            SELECT R.grade, R.comment, B.title
            FROM Rates R
            JOIN BOOK B ON R.ISBN = B.ISBN
            WHERE R.ISBN = ?
        """, (self.isbn,))
        review_data = cursor.fetchall()
        conn.close()

        reviews = ()
        for j in range(len(review_data)):
            reviews += (
                f'Grade: {review_data[j][0]}/10',
                f'Book Title: {review_data[j][2]}',
                f'Review: {review_data[j][1]}',
                '--------------------------------------------------------------------------------------------',
            )

        reviews_var = tk.Variable(value=reviews)

        review_history = tk.Frame(self, bg='#eaddc0')
        review_history.pack(fill=tk.BOTH, expand=True)

        review_listbox = tk.Listbox(
            review_history,
            listvariable=reviews_var,
            height=15,
            width=80,
            selectmode=tk.EXTENDED,
            bg='#eaddc0'
        )

        review_listbox.grid(row=1, column=0)

        back_button = tk.Button(review_history, text="Back", command=self.back, bg='#eaddc0')
        back_button.grid(row=2, column=0, pady=10)

    def back(self):
        self.destroy()
        from book_details_window import BookDetailsWindow
        book_details_window = BookDetailsWindow(self.master, self.isbn)
        book_details_window.grab_set()  # Block interaction with the parent window until it's closed

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg='#eaddc0')
    read_reviews_page = ReadReviews(root, isbn="9783161484100")
    read_reviews_page.pack()
    root.mainloop()