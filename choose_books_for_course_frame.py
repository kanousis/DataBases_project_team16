import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Combobox
from PIL import ImageTk, Image
import sqlite3

class chooseBookFrame(tk.Frame):
    def __init__(self, master, course_id, member_id, semester, curent_academic_year, *args, **kwargs):
        super().__init__(master, bg='#eaddc0', padx=80, *args, **kwargs)
    
        self.course_id=course_id
        self.member_id=member_id
        self.semester=semester
        self.curent_academic_year=curent_academic_year
        self.selected_books = []
        self.var_book_isbn = []
        self.master=master
        self.master.geometry("1000x510")
        self.create_content()
        self.path=""

    def create_content(self):
        color = '#eaddc0'

        self.connection=sqlite3.connect("academia.db")
        self.cursor=self.connection.cursor()
        self.cursor.execute("SELECT title FROM COURSE WHERE course_id=?",(self.course_id,))
        course_name=self.cursor.fetchall()


        text = "Choose Books for Course: "+course_name[0][0]
        tk.Label(self, text=text, bg=color, font=('Arial', 18, 'bold')).grid(row=0, column=0, columnspan=4, pady=10) 

        # Create canvas for Books
        self.canvas_courses = tk.Canvas(self, height=400,width=700, bg=color)
        self.canvas_courses.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        scrollbar_books_vertical = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas_courses.yview)
        scrollbar_books_vertical.grid(row=3, column=1, sticky="ns")
        self.canvas_courses.config(yscrollcommand=scrollbar_books_vertical.set)
        

        books = self.get_books()

        book_frame = tk.Frame(self.canvas_courses, bg=color)
        self.canvas_courses.create_window((0, 0), window=book_frame, anchor="nw")

        book_frame.bind("<Configure>", lambda e: self.canvas_courses.configure(scrollregion=self.canvas_courses.bbox("all")))

        # Bind mouse wheel scrolling
        self.canvas_courses.bind("<Enter>", lambda e: self.canvas_courses.bind_all("<MouseWheel>", self._on_mousewheel))
        self.canvas_courses.bind("<Leave>", lambda e: self.canvas_courses.unbind_all("<MouseWheel>"))


        for i, book in enumerate(books):
            display_title = book[1]
            display_isbn = book[0]
            text = f"{display_title} | ISBN: {display_isbn}"
            selected_book_var = tk.IntVar(value=0)

            # Book label
            book_label = tk.Label(book_frame, text=text, bg=color, font=('Arial', 12, 'bold'))
            book_label.grid(row=i, column=0, padx=10, pady=10, sticky="w")

            # Book checkbox
            book_checkbox = tk.Checkbutton(book_frame, variable=selected_book_var, onvalue=1, offvalue=0)
            book_checkbox.grid(row=i, column=1, padx=10, pady=10)

            # Info button for the book
            info_button = tk.Button(book_frame, text="i", command=lambda isbn=display_isbn: self.book_details_callback(isbn))
            info_button.grid(row=i, column=2, padx=10, pady=10)

            self.var_book_isbn.append((selected_book_var, display_title, display_isbn))


            # Back and Finish buttons
            back_button = tk.Button(self, text="Back", command=self.go_back)
            back_button.grid(row=4, column=0, pady=0, sticky="w")

            finish_button = tk.Button(self, text="Finish", command=self.finish_selection)
            finish_button.grid(row=4, column=1, pady=0, sticky="e")

    def get_books(self):
        self.connection=sqlite3.connect("academia.db")
        self.cursor =  self.connection.cursor()
        self.cursor.execute("SELECT ISBN, title FROM BOOK")
        books=self.cursor.fetchall()
        self.connection.close()
        return books
    

    def book_details_callback(self, isbn):
        isbn = isbn 
        if isbn:  # Check if an ISBN was found
            # Open the book details window
            from book_details_window import BookDetailsWindow
            book_details_window = BookDetailsWindow(self, isbn)
            book_details_window.grab_set()  # Block interaction with the parent window until it's closed
        else:
            print("Book not found")
    

    def go_back(self):
        self.master.destroy()


    def _on_mousewheel(self, event):
        self.canvas_courses.yview_scroll(-1 * (event.delta // 120), "units")



    def finish_selection(self):
        selected_books_count = sum(var.get() for var, _, _ in self.var_book_isbn)
        
        if selected_books_count <= 5:
            selected_books = [(book, isbn) for var, book, isbn in self.var_book_isbn if var.get()]
            self.final_selection(self.member_id, selected_books, self.course_id, self.curent_academic_year)
        else:
            tk.messagebox.showerror("Error", "You can select up to 5 books only!")

        

    def final_selection(self, member_id, total_books, course_id, current_academic_year):
        total_books = total_books 
        # Open the final selection details window
        from final_selection_prof import FinalSelection
        final_selection = FinalSelection(self, member_id, total_books, course_id, current_academic_year)
        final_selection.grab_set()  # Block interaction with the parent window until it's closed   


     