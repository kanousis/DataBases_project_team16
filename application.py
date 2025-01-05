import sqlite3
import tkinter as tk

class ApplicationFrame(tk.Frame):
    def __init__(self, master, student_id, *args, **kwargs):
        super().__init__(master,bg='#eaddc0', *args, **kwargs)
        self.master = master
        self.student_id = student_id
        self.grid(row=0, column=0, sticky="nsew")
        self.master.geometry("1200x1000")
        self.selected_books_by_course = {}
        self.part1_selected_books = []  
        self.part1_var_book_isbn = [] # Holds checkbox values, book titles and ISBNs for part 1 books
        self.part1_var_book_isbn_copy = []        
        self.part2_var_book_isbn = [] # Holds checkbox values, book titles and ISBNs for part 2 books
        self.total_books_var = []  
        self.total_books = [] # Global list to track all selected book names    
        self.connection = sqlite3.connect("academia.db")  
        self.create_content()
    
    def create_content(self):
        semester = self.get_student_semester()
        credits = self.get_student_credits()

        if semester is None:
            tk.Label(self, text="Semester not found", fg="red", bg='#eaddc0').grid(row=0, column=0, padx=10, pady=10)
            return
        
        courses = self.get_courses_for_semester(semester)

        tk.Label(self, text="Textbook Selection", font=("Arial", 18, "bold"), bg='#eaddc0').grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        semester_label = f"Current Semester: {semester}"
        credits_label = f"Credits: {credits:.2f}"
        tk.Label(self, text=semester_label, font=("Arial", 10), bg='#eaddc0').grid(row=1, column=0, padx=10, pady=5, sticky="w")
        tk.Label(self, text=credits_label, font=("Arial", 10), bg='#eaddc0').grid(row=1, column=1, padx=10, pady=5, sticky="w")
    
        # Add explanatory text
        tk.Label(self, text="(*) indicates teacher's suggested book. Not all subjects have a suggested book.", 
        font=("Arial", 10), fg="blue", bg='#eaddc0').grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        # Create canvas for courses
        self.canvas_courses = tk.Canvas(self, height=200, width=1000, bg='#eaddc0')
        self.canvas_courses.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        # Horizontal Scrollbar
        scrollbar_courses_horizontal = tk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.canvas_courses.xview)
        self.canvas_courses.config(xscrollcommand=scrollbar_courses_horizontal.set)
        scrollbar_courses_horizontal.grid(row=4, column=0, sticky="ew")
        
        scrollbar_courses_vertical = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas_courses.yview)
        self.canvas_courses.config(yscrollcommand=scrollbar_courses_vertical.set)
        scrollbar_courses_vertical.grid(row=3, column=1, sticky="ns")
        
        courses_frame = tk.Frame(self.canvas_courses, width=1000, bg='#eaddc0')
        tk.Label(courses_frame, text="Subjects:", font=("Arial", 12, "bold"), bg='#eaddc0').grid(row=0, column=0, padx=10, pady=5, sticky="w")

        courses_frame.bind("<Configure>", lambda e: self.canvas_courses.configure(scrollregion=self.canvas_courses.bbox("all")))
        # Bind mouse wheel scrolling
        self.canvas_courses.bind("<Enter>", lambda e: self.canvas_courses.bind_all("<MouseWheel>", self._on_mousewheel))
        self.canvas_courses.bind("<Leave>", lambda e: self.canvas_courses.unbind_all("<MouseWheel>"))

        cursor = self.connection.cursor()
        query = """
            SELECT B.title, B.ISBN, C.course_id, P.book_suggestion, C.semester
            FROM BOOK B
            JOIN PARTICIPATES P ON B.ISBN = P.ISBN
            JOIN COURSE C ON P.course_id = C.course_id
        """
        cursor.execute(query)
        books = cursor.fetchall()
        cursor.close()
        books_dict = {}
        part2_books_dict = {}
        
        for book_title, isbn, course_id, suggestion, book_semester in books:
            if course_id not in books_dict:
                books_dict[course_id] = []
            if book_semester == semester:
                books_dict[course_id].append((book_title, suggestion, isbn))
            
            if course_id not in part2_books_dict:
                part2_books_dict[course_id] = []
            part2_books_dict[course_id].append((book_title, isbn))
        if courses:

            for i, (course_name, course_id) in enumerate(courses):
                tk.Label(courses_frame, text=course_name, bg='#eaddc0').grid(row=i+1, column=0, padx=10, pady=5, sticky="w")
                
                # Frame to hold the dropdown and the "i" button
                book_frame = tk.Frame(courses_frame, bg='#eaddc0')

                books_for_course = books_dict.get(course_id, [])
                for j, (book_title, suggestion, isbn) in enumerate(books_for_course):
                    # Add asterisk for suggested books
                    display_name = f"{book_title} (*)" if suggestion else book_title
                    selected_book_var = tk.IntVar(value=0)
                    # Create label for the book
                    book_label = tk.Label(book_frame, text=display_name, width=50, anchor="w", bg='#eaddc0')
                    book_label.pack(side="left", padx=5)
                    
                    # Create a checkbox for the book
                    book_checkbox = tk.Checkbutton(
                        book_frame, variable=selected_book_var, onvalue=j+1, offvalue=0, bg='#eaddc0',
                        command=lambda course_name=course_name, course_id=course_id, 
                        selected_book_var=selected_book_var, book_title=book_title, 
                        isbn=isbn: self.check_book_selection(course_name, course_id, selected_book_var, book_title, isbn)
                    )
                    book_checkbox.pack(side="left", padx=5)

                    self.part1_var_book_isbn.append((selected_book_var, book_title, isbn))                   
                    
                    # Info button for the book
                    info_button = tk.Button(book_frame, text="i", command=lambda isbn=isbn: self.book_details_callback(isbn))
                    
                    info_button.pack(side="left", padx=5)

                # Add the book frame to the courses frame
                book_frame.grid(row=i+1, column=1, padx=10, pady=5, sticky="w")

        else:
            tk.Label(courses_frame, text="No subjects found for this semester", fg="gray", bg='#eaddc0').grid(row=1, column=0, padx=10, pady=5)

        self.canvas_courses.create_window((0, 0), window=courses_frame, anchor="nw")
        courses_frame.update_idletasks()
        self.canvas_courses.config(scrollregion=self.canvas_courses.bbox("all"))

        # Label for additional books section
        tk.Label(self, text="Select Additional Books", font=("Arial", 18, "bold"), bg='#eaddc0').grid(row=5, column=0, columnspan=2, padx=10, pady=10)
        # Add explanatory text
        tk.Label(self, text="(x) indicates book's credits.", 
        font=("Arial", 10), fg="blue", bg='#eaddc0').grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        # Create canvas for additional books
        self.canvas_additional_books = tk.Canvas(self, height=200, width=1000, bg='#eaddc0')
        self.canvas_additional_books.grid(row=7, column=0, padx=10, pady=10, sticky="nsew")

        # Horizontal Scrollbar
        scrollbar_additional_books_horizontal = tk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.canvas_additional_books.xview)
        self.canvas_additional_books.config(xscrollcommand=scrollbar_additional_books_horizontal.set)
        scrollbar_additional_books_horizontal.grid(row=8, column=0, sticky="ew")        
        
        scrollbar_additional_books = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas_additional_books.yview)
        self.canvas_additional_books.config(yscrollcommand=scrollbar_additional_books.set)
        scrollbar_additional_books.grid(row=7, column=1, sticky="ns")
        
        additional_books_frame = tk.Frame(self.canvas_additional_books, width=1000, bg='#eaddc0')
        tk.Label(additional_books_frame, text="All Subjects:", font=("Arial", 12, "bold"), bg='#eaddc0').grid(row=0, column=0, padx=10, pady=5, sticky="w")

        additional_books_frame.bind("<Configure>", lambda e: self.canvas_additional_books.configure(scrollregion=self.canvas_additional_books.bbox("all")))
        # Bind mouse wheel scrolling
        self.canvas_additional_books.bind("<Enter>", lambda e: self.canvas_additional_books.bind_all("<MouseWheel>", self._on_mousewheel_additional_books))
        self.canvas_additional_books.bind("<Leave>", lambda e: self.canvas_additional_books.unbind_all("<MouseWheel>"))


        all_courses = self.get_all_courses()
        # List to store the selected books and their credits
        self.selected_books = []
        
        for i, (course_name, course_id) in enumerate(all_courses):
            tk.Label(additional_books_frame, text=course_name, bg='#eaddc0').grid(row=i+1, column=0, padx=10, pady=5, sticky="w")
            
            # Frame to hold the checkboxes and the "i" button
            book_frame = tk.Frame(additional_books_frame, bg='#eaddc0')

            part2_books_for_course = part2_books_dict.get(course_id, [])   
            for j, (book_title, isbn) in enumerate(part2_books_for_course):
                
                # Get the book's credits from your data 
                credits = self.get_book_credits(isbn)  

                # Create a variable to store the state of the checkbox (1 = selected, 0 = not selected)
                book_var = tk.IntVar(value=0)  # Initially, no checkbox is selected
                
                # Store the checkbox variable and credits in the selected_books list
                self.selected_books.append((book_var, credits))
                self.part2_var_book_isbn.append((book_var, book_title, isbn))

                # Create label for the book
                book_label = tk.Label(book_frame, text=f"({credits:.2f}){book_title}", width=50, anchor="w", bg='#eaddc0')
                book_label.pack(side="left", padx=5)
                
                # Create a checkbox for the book
                book_checkbox = tk.Checkbutton(book_frame, variable=book_var, bg='#eaddc0')
                book_checkbox.pack(side="left", padx=5)
                
                # Info button for the book
                info_button = tk.Button(book_frame, text="i", command=lambda isbn=isbn: self.book_details_callback(isbn))
                info_button.pack(side="left", padx=5)
            
            # Add the book frame to the courses frame
            book_frame.grid(row=i+1, column=1, padx=10, pady=5, sticky="w")

        
        # Button to check credits
        check_button = tk.Button(self, text="Check Credits", command=self.check_credits, bg='#eaddc0')
        check_button.grid(row=9 + len(courses) + len(all_courses), column=0, columnspan=2, pady=20)

        # Label for displaying credit result
        self.credit_result_label = tk.Label(self, text="", bg='#eaddc0', fg='black')
        self.credit_result_label.grid(row=10 + len(courses) + len(all_courses), column=0, columnspan=2)

        self.canvas_additional_books.create_window((0, 0), window=additional_books_frame, anchor="nw")
        additional_books_frame.update_idletasks()
        self.canvas_additional_books.config(scrollregion=self.canvas_additional_books.bbox("all"))

        # Back and Finish buttons
        back_button = tk.Button(self, text="Back", command=self.go_back, bg='#eaddc0')
        back_button.grid(row=11 + len(courses) + len(all_courses), column=0, pady=20)

        finish_button = tk.Button(self, text="Finish", command=self.finish_selection, bg='#eaddc0')
        finish_button.grid(row=11 + len(courses) + len(all_courses), column=1, pady=20)

    def _on_mousewheel(self, event):
        self.canvas_courses.yview_scroll(-1 * (event.delta // 120), "units")

    def _on_mousewheel_additional_books(self, event):
        self.canvas_additional_books.yview_scroll(-1 * (event.delta // 120), "units")

    def get_student_semester(self):
        
        cursor = self.connection.cursor()
        query = "SELECT current_semester FROM STUDENT WHERE student_id = ?"
        cursor.execute(query, (self.student_id,))
        semester = cursor.fetchone()
        cursor.close()
        #
        return semester[0] if semester else None

    def get_student_credits(self):
        cursor = self.connection.cursor()
        query = "SELECT credits FROM STUDENT WHERE student_id = ?"
        cursor.execute(query, (self.student_id,))
        credits = cursor.fetchone()
        cursor.close()
        #
        return credits[0] if credits else 0

    def get_courses_for_semester(self, semester):
        cursor = self.connection.cursor()
        query = "SELECT title, course_id FROM COURSE WHERE semester = ?"
        cursor.execute(query, (semester,))
        courses = cursor.fetchall()
        cursor.close()
        #
        return courses

    def get_all_courses(self):
        cursor = self.connection.cursor()
        query = "SELECT title, course_id FROM COURSE"
        cursor.execute(query)
        courses = cursor.fetchall()
        cursor.close()
        #
        return courses

    def get_books_for_semester(self):
        # Get the current semester of the student
        semester = self.get_student_semester()
        if semester is None:
            return []  # Return an empty list if semester is not found

        # Get the courses for the current semester
        courses = self.get_courses_for_semester(semester)
        if not courses:
            return []  # Return an empty list if no courses are found

        # List to hold all the books
        all_books_isbns = []

        # Database connection
        cursor = self.connection.cursor()

        # Fetch books for each course
        for course,isbn in courses:
            query = """
                SELECT B.ISBN
                FROM BOOK B
                JOIN PARTICIPATES P ON B.ISBN = P.ISBN
                JOIN COURSE C ON P.course_id = C.course_id
                WHERE C.title = ?
            """
            cursor.execute(query, (course,))
            books = cursor.fetchall()

            # Append books to the list
            all_books_isbns.extend([book[0] for book in books])

        # Close the database connection
        cursor.close()
        
        return all_books_isbns

    def check_book_selection(self, course_name, course_id, selected_book_var, book_title, isbn):
        # This function is called every time a checkbox is toggled. It checks if more than one checkbox is selected for the same course.
        if course_id not in self.selected_books_by_course:
            self.selected_books_by_course[course_id] = []

        # Get the list of selected books for the current course
        selected_books_for_this_course = self.selected_books_by_course[course_id]

        if selected_book_var.get() == 0:
            if (selected_book_var, book_title, isbn) in selected_books_for_this_course:
                 selected_books_for_this_course.remove((selected_book_var, book_title, isbn))
        else:
            selected_books_for_this_course.append((selected_book_var, book_title, isbn))
            # Check if there are multiple selected books for the same course
            if len(selected_books_for_this_course) > 1:
                tk.messagebox.showerror("Error", f"You can only select one book for the course: {course_name}")
                selected_books_for_this_course.remove((selected_book_var, book_title, isbn))
                selected_book_var.set(0)  # Uncheck the book if more than one is selected

    def go_back(self):
        self.connection.close()
        from home_page import WelcomeFrame
        self.destroy()
        purchase_frame = WelcomeFrame(self.master, member_id=self.student_id)
        purchase_frame.pack()

    def book_details_callback(self, isbn):
        if isbn:  # Check if an ISBN was found
            # Open the book details window
            from book_details_window import BookDetailsWindow
            book_details_window = BookDetailsWindow(self, isbn)
            book_details_window.grab_set()  # Block interaction with the parent window until it's closed
        else:
            print("Book not found")

    def check_credits(self):
        """Calculate the total credits for selected books and check if the student has enough credits."""
        total_credits = 0
        for var, credits in self.selected_books:
            if var.get():  # If the checkbox is selected
                total_credits += credits

        available_credits = self.get_student_credits()  # This should return the available credits for the student
        remaining_credits = round(available_credits - total_credits, 2)

        # Update the credit result label
        if remaining_credits >= 0:
            self.credit_result_label.config(
                text=f"You can select these books. Remaining credits: {remaining_credits}", fg="green")
        else:
            self.credit_result_label.config(
                text=f"Not enough credits! You need {abs(remaining_credits)} more credits.", fg="red")
    
    def get_book_credits(self, isbn):
        cursor = self.connection.cursor()
        query = "SELECT credits FROM BOOK WHERE ISBN = ?"
        cursor.execute(query, (isbn,))
        credits = cursor.fetchone()
        cursor.close()
        #
        return credits[0] if credits else 0  # Return the credits or 0 if not found
    
    def finish_selection(self):
        """Check credits and proceed to the final page if all conditions are met."""
        total_credits = 0
        for var, credits in self.selected_books:
            if var.get():  # If the checkbox is selected
                total_credits += credits # total application credits for selected books

        available_credits = self.get_student_credits()
        remaining_credits = available_credits - total_credits

        if remaining_credits >= 0:
            self.part1_var_book_isbn_copy.clear()
            self.part1_selected_books.clear()
            self.part1_var_book_isbn_copy.extend(self.part1_var_book_isbn)
            part1_selected_books_copy = []
            
            for var, book, isbn in self.part1_var_book_isbn_copy:
                if var.get():  # If the checkbox is selected
                    self.part1_selected_books.append((var, book, isbn)) # list of part 1 selected books
                    part1_selected_books_copy.append((book, isbn))
                
            if self.part1_selected_books:
                    all_semester_books_isbns = self.get_books_for_semester()
                    valid_selection = True

                    for isbn in all_semester_books_isbns:
                        if part1_selected_books_copy.count(isbn) >= 2:
                            tk.messagebox.showerror("Error", "You have selected the same book for multiple different subjects!")
                            valid_selection = False
                            break
                        else: 
                            continue
                    if valid_selection:
                        self.total_books.clear()
                        self.total_books_var.clear()
                        self.total_books_var.extend(self.part1_selected_books)
                        self.total_books_var.extend(self.part2_var_book_isbn)
                        for var, book, isbn in self.total_books_var:
                            if var.get():  # If the checkbox is selected
                                self.total_books.append((book, isbn))

                        # Open the summary page with selected books
                        self.final_selection(self.student_id, self.total_books, self.get_student_semester(), remaining_credits, total_credits)
            else:
                tk.messagebox.showerror("Error", "No books selected for current semester!")
        else:
            # Display an error message
            tk.messagebox.showerror("Error", "You have selected more books than your available credits!")

    def final_selection(self, student_id,total_books, semester, remaining_credits, application_credits):
        

        if total_books:  
            # Open the book details window
            from final_selection import FinalSelection
            final_selection = FinalSelection(self, student_id,total_books, semester, remaining_credits, application_credits)
            final_selection.grab_set()  # Block interaction with the parent window until it's closed
        else:
            print("No books selected.")