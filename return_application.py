import tkinter as tk
import sqlite3
import datetime
import hashlib

class ReturnApplicationFrame(tk.Frame):
    def __init__(self, master, student_id):
        super().__init__(master, bg='#eaddc0')
        self.master = master
        self.master.geometry("700x500")
        self.student_id = student_id
        self.counter = 0
        self.total_books = []
        self.pack(fill="both", expand=True)  # Ensure the frame is packed
        self.create_content()

    def create_content(self):
        tk.Label(self, text="Return Selection", font=("Arial", 18, "bold"), bg='#eaddc0').grid(row=0, column=0, columnspan=2, padx=10, pady=10)
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

        self.get_books()

        if self.total_books:
            self.connection = sqlite3.connect("academia.db")
            cursor = self.connection.cursor()
            self.selected_pickup_points = []  # List to store selected pickup points

            for i, (book, isbn) in enumerate(self.total_books, start=1):
                tk.Label(books_frame, text=book, bg='#eaddc0').grid(row=i+1, column=0, padx=10, pady=5, sticky="w")
            
                # Frame to hold the dropdown and the "i" button
                pickup_point_frame = tk.Frame(books_frame, bg='#eaddc0')
                pickup_point_frame.grid(row=i+1, column=1, padx=10, pady=5, sticky="w")

                # Fetch pickup points for the book
                query = """
                    SELECT P.name, P.street, P.number, P.telephone, P.pickup_point_id
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
                    f"{name} | {street} {number} | {telephone} | {pickup_point_id}" 
                    for name, street, number, telephone, pickup_point_id in pickup_points
                ])
                pickup_point_menu.pack(side="left", padx=5)

                # Append the selected pickup point to the list
                self.selected_pickup_points.append((pickup_point_var, isbn, None))
                
        else:
            tk.Label(books_frame, text="No subjects found for this semester", fg="gray", bg='#eaddc0').grid(row=1, column=0, padx=10, pady=5)

        self.canvas_books.create_window((0, 0), window=books_frame, anchor="nw")
        books_frame.update_idletasks()
        self.canvas_books.config(scrollregion=self.canvas_books.bbox("all"))

        # Back and Finish buttons
        back_button = tk.Button(self, text="Back", command=self.go_back, bg='#eaddc0')
        back_button.grid(row=3+len(self.total_books), column=0, pady=20)

        complete_button = tk.Button(
            self,
            text="Complete Application",
            command=lambda: self.complete_application(),
            bg='#eaddc0'
        )
        complete_button.grid(row=4+len(self.total_books), column=0, pady=20)

    def _on_mousewheel(self, event):
        self.canvas_books.yview_scroll(-1 * (event.delta // 120), "units")

    def complete_application(self):
        connection = sqlite3.connect("academia.db")
        cursor = connection.cursor()

        date = datetime.date.today().strftime("%Y-%m-%d")

        # Extract actual values from StringVar objects
        selected_pickup_points = []  # List to store pairs of (ISBN, selected pickup point)
        for item in self.selected_pickup_points:
            value = item[0].get()
            if value != "Select Pickup Point":
                # Extract the pickup_point_id from the selected value
                pickup_point_id = value.split(" | ")[-1]
                selected_pickup_points.append((item[1], pickup_point_id))

        # Check if a bookstore has been selected for each ISBN
        if len(selected_pickup_points) == 0:
            tk.messagebox.showerror("Error", "Please select a bookstore for at least one book.")
            return

        # Insert into RETURN table for each book
        for isbn, pickup_point_id in selected_pickup_points:
            string = f"{self.student_id}{isbn}{datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')}"
            return_id = int(hashlib.sha256(string.encode()).hexdigest(), 16) % 10**18  # Limit to 18 digits (sqlite integer limit)
            return_application_query = """
                INSERT INTO RETURN (return_id, date, student_id, pickup_point_id)
                VALUES (?, ?, ?, ?)
            """
            cursor.execute(return_application_query, (return_id, date, self.student_id, pickup_point_id))
            connection.commit()

            # Insert into Contains(RETURN-BOOK) table
            contains_query = """
                INSERT INTO "Contains(RETURN-BOOK)" (return_id, ISBN)
                VALUES (?, ?)
            """
            cursor.execute(contains_query, (return_id, isbn))


            # Fetch the credits of the book
            credits_query = """
                SELECT credits
                FROM BOOK
                WHERE ISBN = ?
            """
            cursor.execute(credits_query, (isbn,))
            book_credits = cursor.fetchone()[0]

            # Fetch the current credits of the student
            cursor.execute("SELECT credits FROM STUDENT WHERE student_id = ?", (self.student_id,))
            student_credits = cursor.fetchone()[0]
             
            # Calculate the new total credits
            new_total_credits = student_credits + book_credits

            # Update the student's credits
            update_credits_query = """
                UPDATE STUDENT
                SET credits = ?
                WHERE student_id = ?
            """
            cursor.execute(update_credits_query, (new_total_credits, self.student_id))
             
        connection.commit()
        connection.close()
        tk.messagebox.showinfo("Application Completed", "Your application has been successfully completed!")
        self.go_back()


    def get_books(self):
        conn = sqlite3.connect("academia.db")

        self.cursor = conn.execute("SELECT C.ISBN, B.title\
                                  FROM APPLICATION AS A\
                                  INNER JOIN STUDENT AS S ON A.student_id = S.student_id\
                                  INNER JOIN Consists_Of AS C ON A.application_id = C.application_id\
                                  INNER JOIN BOOK AS B ON C.ISBN = B.ISBN\
                                  WHERE A.semester < S.current_semester AND S.student_id=?", (self.student_id,))
        
        data1 = self.cursor.fetchall()

        self.cursor = conn.execute("SELECT CRB.ISBN, B.title\
                                 FROM RETURN AS R\
                                 INNER JOIN [Contains(RETURN-BOOK)] AS CRB ON R.return_id = CRB.return_id\
                                 INNER JOIN BOOK AS B ON CRB.ISBN = B.ISBN\
                                 WHERE R.student_id=?", (self.student_id,))
        data2 = self.cursor.fetchall()
        data = list(set(data1) - set(data2))

        conn.close()
        for isbn, title in data:
            self.total_books.append((title, isbn))

    def go_back(self):
        self.connection.close()
        from home_page import WelcomeFrame
        self.destroy()
        purchase_frame = WelcomeFrame(self.master, member_id=self.student_id)
        purchase_frame.pack()

