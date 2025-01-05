import tkinter as tk
import sqlite3
import datetime

class FinalSelection(tk.Toplevel):
    def __init__(self, master, student_id, total_books, semester, remaining_credits, application_credits):
        super().__init__(master)
        self.title("Final Selection")
        self.total_books = total_books
        self.master = master
        self.student_id = student_id
        self.semester = semester
        self.remaining_credits = remaining_credits
        self.application_credits = application_credits
        self.geometry("700x500")
        self.configure(bg='#eaddc0')
        self.create_content()

    def create_content(self):
        tk.Label(self, text="Final Selection", font=("Arial", 18, "bold"), bg='#eaddc0').grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        # Create canvas for books
        self.canvas_books = tk.Canvas(self, height=300, width=600, bg='#eaddc0')
        self.canvas_books.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        # Create vertical scrollbar for the canvas
        scrollbar_books = tk.Scrollbar(self, orient="vertical", command=self.canvas_books.yview)
        scrollbar_books.grid(row=1, column=1, sticky="ns")
        self.canvas_books.configure(yscrollcommand=scrollbar_books.set)   

        books_frame = tk.Frame(self.canvas_books, bg='#eaddc0')
        tk.Label(books_frame, text="Total Books:", font=("Arial", 12, "bold"), bg='#eaddc0').grid(row=0, column=0, padx=10, pady=5, sticky="w")

        books_frame.bind("<Configure>", lambda e: self.canvas_books.configure(scrollregion=self.canvas_books.bbox("all")))
        # Bind mouse wheel scrolling
        self.canvas_books.bind("<Enter>", lambda e: self.canvas_books.bind_all("<MouseWheel>", self._on_mousewheel))
        self.canvas_books.bind("<Leave>", lambda e: self.canvas_books.unbind_all("<MouseWheel>"))

        if self.total_books:
            connection = sqlite3.connect("academia.db")
            cursor = connection.cursor()
            self.selected_pickup_points = []  # List to store selected pickup points
            for i, (book, isbn) in enumerate(self.total_books, start=1):
                tk.Label(books_frame, text=book, bg='#eaddc0').grid(row=i+1, column=0, padx=10, pady=5, sticky="w")
            
                # Frame to hold the dropdown and the "i" button
                pickup_point_frame = tk.Frame(books_frame, bg='#eaddc0')
                pickup_point_frame.grid(row=i+1, column=1, padx=10, pady=5, sticky="w")

                # Fetch pickup points for the book
                query = """
                    SELECT P.name, P.street, P.number, P.telephone
                    FROM PICKUP_POINT P
                    JOIN It_Has I ON P.pickup_point_id = I.pickup_point_id
                    WHERE I.ISBN = ?
                """
                cursor.execute(query, (isbn,))
                pickup_points = cursor.fetchall()

                # Create a dropdown menu for pickup points
                pickup_point_var = tk.StringVar(pickup_point_frame)
                pickup_point_var.set("Select Pickup Point")
                pickup_point_menu = tk.OptionMenu(pickup_point_frame, pickup_point_var, *[
                    f"{name} | {street} {number} | {telephone}" for name, street, number, telephone in pickup_points
                ])
                pickup_point_menu.config(bg='#eaddc0')
                pickup_point_menu.pack(side="left", padx=5)

                # Append the selected pickup point to the list
                self.selected_pickup_points.append((pickup_point_var, isbn))
                
        else:
            tk.Label(books_frame, text="No subjects found for this semester", fg="gray", bg='#eaddc0').grid(row=1, column=0, padx=10, pady=5)

        self.canvas_books.create_window((0, 0), window=books_frame, anchor="nw")
        books_frame.update_idletasks()
        self.canvas_books.config(scrollregion=self.canvas_books.bbox("all"))


        # Back and Finish buttons
        back_button = tk.Button(self, text="Back", command=self.destroy, bg='#eaddc0')
        back_button.grid(row=3+len(self.total_books), column=0, pady=20)

        complete_button = tk.Button(
            self,
            text="Complete Application",
            command=lambda: self.complete_application(),
            bg='#eaddc0'
        )
        complete_button.grid(row=4+len(self.total_books), column=0, pady=20)

    def complete_application(self):
        connection = sqlite3.connect("academia.db")
        cursor = connection.cursor()

        # Generate application_id
        application_id = int(f"{self.student_id}{self.semester}")
        date = datetime.date.today().strftime("%Y-%m-%d")

        # Check if application already exists
        check_query = "SELECT COUNT(*) FROM APPLICATION WHERE application_id = ?"
        cursor.execute(check_query, (application_id,))
        exists = cursor.fetchone()[0]

        if exists:
            # Delete existing application and associated records
            delete_application_query = "DELETE FROM APPLICATION WHERE application_id = ?"
            delete_consists_of_query = "DELETE FROM Consists_Of WHERE application_id = ?"
            cursor.execute(delete_application_query, (application_id,))
            cursor.execute(delete_consists_of_query, (application_id,))

        # Insert into APPLICATION table
        application_query = """
            INSERT INTO APPLICATION (application_id, date, semester, student_id, application_credits)
            VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(application_query, (application_id, date, self.semester, self.student_id, self.application_credits))

        # Insert into Consists_Of table
        consists_of_query = """
            INSERT INTO Consists_Of (application_id, ISBN)
            VALUES (?, ?)
        """
        for book, isbn in self.total_books:
            cursor.execute(consists_of_query, (application_id, isbn))
    
        # Update the student's credits
        update_credits_query = """
            UPDATE STUDENT
            SET credits = ?
            WHERE student_id = ?
        """
        cursor.execute(update_credits_query, (self.remaining_credits, self.student_id))

        connection.commit()
        connection.close()
        tk.messagebox.showinfo("Application Completed", "Your application has been successfully completed!")
        self.destroy()

    def _on_mousewheel(self, event):
        self.canvas_books.yview_scroll(-1 * (event.delta // 120), "units")