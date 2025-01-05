import tkinter as tk
import sqlite3
import datetime

class OldApplicationFrame(tk.Frame):
    def __init__(self, master, student_id, application_id):
        super().__init__(master)
        self.application_id = application_id
        self.master = master
        self.student_id = student_id
        self.master.geometry("600x600")
        self.configure(bg='#eaddc0')
        self.create_content()

    def create_content(self):
        tk.Label(self, text="Preview Old Application", font=("Arial", 18, "bold"), bg='#eaddc0').grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        # Create canvas for books
        self.canvas_books = tk.Canvas(self, height=300, width=500, bg='#eaddc0')
        self.canvas_books.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Create vertical scrollbar for the canvas
        scrollbar_books = tk.Scrollbar(self, orient="vertical", command=self.canvas_books.yview)
        scrollbar_books.grid(row=1, column=1, sticky="ns")
        self.canvas_books.configure(yscrollcommand=scrollbar_books.set)  

        books_frame = tk.Frame(self.canvas_books, bg='#eaddc0')
        tk.Label(books_frame, text="Your old application consists of the following books:", font=("Arial", 12, "bold"), bg='#eaddc0').grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        books_frame.bind("<Configure>", lambda e: self.canvas_books.configure(scrollregion=self.canvas_books.bbox("all")))
        # Bind mouse wheel scrolling
        self.canvas_books.bind("<Enter>", lambda e: self.canvas_books.bind_all("<MouseWheel>", self._on_mousewheel))
        self.canvas_books.bind("<Leave>", lambda e: self.canvas_books.unbind_all("<MouseWheel>"))

        # Connect to the database
        connection = sqlite3.connect('academia.db')
        cursor = connection.cursor()

        # Query to get the books for the given application_id
        query = """
            SELECT B.title, B.ISBN
            FROM BOOK B
            JOIN Consists_Of C ON B.ISBN = C.ISBN
            WHERE C.application_id = ?
        """
        cursor.execute(query, (self.application_id,))
        self.total_books = cursor.fetchall()

        connection.close()
        if self.total_books:
            for i, (book, isbn) in enumerate(self.total_books, start=1):
                tk.Label(books_frame, text=book, bg='#eaddc0').grid(row=i+1, column=0, padx=10, pady=5, sticky="w")
        else:
            tk.Label(books_frame, text="No subjects found for this semester", fg="gray", bg='#eaddc0').grid(row=1, column=0, padx=10, pady=5)

        self.canvas_books.create_window((0, 0), window=books_frame, anchor="nw")
        books_frame.update_idletasks()
        self.canvas_books.config(scrollregion=self.canvas_books.bbox("all"))

        # Back and Finish buttons
        back_button = tk.Button(self, text="Back to homepage", command=self.go_back, bg='#eaddc0')
        back_button.grid(row=3+len(self.total_books), column=0, pady=20)

        caution_label = tk.Label(
            self,
            text="Caution: If you continue to a new application, your previous application will be deleted.",
            font=("Arial", 10, "bold"),
            fg="red",
            bg='#eaddc0'
        )
        caution_label.grid(row=4+len(self.total_books), column=0, padx=10, pady=10)
        
        complete_button = tk.Button(
            self,
            text="Make a new application",
            command=lambda: self.complete_application(),
            bg='#eaddc0'
        )
        complete_button.grid(row=5+len(self.total_books), column=0, pady=20)

    def complete_application(self):
        connection = sqlite3.connect("academia.db")
        cursor = connection.cursor()

        # Check if application already exists
        check_query = "SELECT COUNT(*) FROM APPLICATION WHERE application_id = ?"
        cursor.execute(check_query, (self.application_id,))
        exists = cursor.fetchone()[0]

        if exists:
            check_query = "SELECT application_credits FROM APPLICATION WHERE application_id = ?"
            cursor.execute(check_query, (self.application_id,))
            application = cursor.fetchone()
            application_credits = application[0]
            cursor.execute("SELECT credits FROM STUDENT WHERE student_id = ?", (self.student_id,))
            student_credits = cursor.fetchone()[0]
            # Add the previous application's credits to the student's credits
            new_credits = student_credits + application_credits
            update_credits_query = "UPDATE STUDENT SET credits = ? WHERE student_id = ?"
            cursor.execute(update_credits_query, (new_credits, self.student_id))
                       
            # Delete existing application and associated records
            delete_application_query = "DELETE FROM APPLICATION WHERE application_id = ?"
            delete_consists_of_query = "DELETE FROM Consists_Of WHERE application_id = ?"
            cursor.execute(delete_application_query, (self.application_id,))
            cursor.execute(delete_consists_of_query, (self.application_id,))

        connection.commit()
        connection.close()
        tk.messagebox.showinfo("Old Application Deleted", "Your old application has been successfully deleted! You can now create a new application.")
  
        from application import ApplicationFrame
        if hasattr(self, 'application_frame'):
            return
        # Proceed to the application frame
        self.destroy()
        self.application_frame = ApplicationFrame(self.master, student_id=self.student_id)
        self.application_frame.pack()

    def go_back(self):
        #self.connection.close()
        from home_page import WelcomeFrame
        self.destroy()
        purchase_frame = WelcomeFrame(self.master, member_id=self.student_id)
        purchase_frame.pack()


    def _on_mousewheel(self, event):
        self.canvas_books.yview_scroll(-1 * (event.delta // 120), "units")