import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Combobox
from PIL import ImageTk, Image
import sqlite3
import io

class RatingFrame(tk.Frame):
    def __init__(self, master, book_item, member_id, *args, **kwargs):
        super().__init__(master, bg='#eaddc0', padx=80, *args, **kwargs)
        self.member_id=member_id
        self.book_item=book_item
        self.master=master
        self.master.geometry("800x500")
        self.create_content()
        self.path=""

    def create_content(self):
        color1 = '#eaddc0'
        color2 = '#eaddc0'
        color3 = '#eaddc0'
        left_frame = tk.Frame(self, bg=color1)
        left_frame.grid(column=0,row=0,columnspan=2)

        right_frame = tk.Frame(self, bg=color2)
        right_frame.grid(column=2,row=0,columnspan=1)

        middle_frame = tk.Frame(self, bg=color3)
        middle_frame.grid(column=0,row=2,columnspan=4)


        conn=sqlite3.connect("academia.db")
        cursor=conn.execute("SELECT ISBN, title, author, cover, pages_number, publisher, credits\
                            FROM BOOK\
                            WHERE ISBN=?",(self.book_item,))
        data=cursor.fetchall()
        conn.close()


        image_data = io.BytesIO(data[0][3])
        book_cover = Image.open(image_data)
        book_cover = book_cover.resize((200, 250))  
        book_cover = ImageTk.PhotoImage(book_cover)

        # Display the image and book details
        cover_label = tk.Label(left_frame, image=book_cover)
        cover_label.image = book_cover
        cover_label.grid(column=0, row=0)

        book_label = tk.Label(right_frame, text="ISBN: ",bg=color1,fg='black',font=('Calibri', 12, 'bold'))
        book_label_1 = tk.Label(right_frame, text=data[0][0],bg=color1,fg='black',font=('Calibri', 12, 'bold'))
        title_label = tk.Label(right_frame, text="Title: ",bg=color1,fg='black',font=('Calibri', 12, 'bold'))
        title_label_1 = tk.Label(right_frame, text=data[0][1],bg=color1,fg='black',font=('Calibri', 12, 'bold'))
        author_label = tk.Label(right_frame, text="Author: ",bg=color1,fg='black',font=('Calibri', 12, 'bold'))
        author_label_1 = tk.Label(right_frame, text=data[0][2],bg=color1,fg='black',font=('Calibri', 12, 'bold'))
        pages_label = tk.Label(right_frame, text="Pages: ",bg=color1,fg='black',font=('Calibri', 12, 'bold'))
        pages_label_1 = tk.Label(right_frame, text=data[0][4],bg=color1,fg='black',font=('Calibri', 12, 'bold'))
        publisher_label = tk.Label(right_frame, text="Publisher: ",bg=color1,fg='black',font=('Calibri', 12, 'bold'))
        publisher_label_1 = tk.Label(right_frame, text=data[0][5],bg=color1,fg='black',font=('Calibri', 12, 'bold'))
        credits_label = tk.Label(right_frame, text="Credits: ",bg=color1,fg='black',font=('Calibri', 12, 'bold'))
        credits_label_1 = tk.Label(right_frame, text=data[0][6],bg=color1,fg='black',font=('Calibri', 12, 'bold'))


        book_label.grid(column=0,row=0, sticky='e')
        book_label_1.grid(column=1,row=0, sticky='w')
        title_label.grid(column=0,row=1, sticky='e')
        title_label_1.grid(column=1,row=1, sticky='w')
        author_label.grid(column=0,row=2, sticky='e')
        author_label_1.grid(column=1,row=2, sticky='w')
        pages_label.grid(column=0,row=3, sticky='e')
        pages_label_1.grid(column=1,row=3, sticky='w')
        publisher_label.grid(column=0,row=4, sticky='e')
        publisher_label_1.grid(column=1,row=4, sticky='w')
        credits_label.grid(column=0,row=5, sticky='e')
        credits_label_1.grid(column=1,row=5, sticky='w')

        conn = sqlite3.connect("academia.db")
        cursor = conn.cursor()

        # Check if there is already a rating for this ISBN and student_id
        cursor.execute(
            "SELECT * FROM Rates WHERE ISBN = ? AND student_id = ?",
            (self.book_item, self.member_id)
        )
        existing_rating = cursor.fetchone()
        if existing_rating:
            rating_label_1 = tk.Label(right_frame, text="You have already rated this book!",bg=color1,fg='red',font=('Calibri', 12, 'bold'))
            rating_label_2 = tk.Label(right_frame, text="You can change the previous rating by making a new submission.",bg=color1,fg='red',font=('Calibri', 12, 'bold'))
            rating_label_1.grid(column=0,row=6, columnspan=2, sticky='w')
            rating_label_2.grid(column=0,row=7, columnspan=2, sticky='w')

            

        rating_label = tk.Label(middle_frame, text="Rate this book:",bg=color3,fg='black',font=('Calibri', 12, 'bold'))
        rating_label.grid(column=0, row=0, columnspan=1, sticky='e')
        ratings = [round(i * 0.5, 1) for i in range(2, 21)]  # [1.0, 1.5, ..., 10.0]
        self.rating_dropdown = Combobox(middle_frame, values=ratings, state="readonly", font=('Calibri', 12), width=10)
        self.rating_dropdown.grid(column=1, row=0, pady=5, sticky='e')

        comment_label = tk.Label(middle_frame, text="Write a comment:", bg=color3, fg='black', font=('Calibri', 12, 'bold'))
        comment_label.grid(column=0, row=1, columnspan=1, sticky='e')
        self.comment_text = tk.Text(middle_frame, width=30, height=8, font=('Calibri', 12))
        self.comment_text.grid(column=1, row=1, pady=5)


        submit_btn = tk.Button(middle_frame,text="Submit",command=lambda: self.submitBtn())
        submit_btn.grid(column=1, row=2, columnspan=1, sticky='e')


        back_btn=tk.Button(middle_frame,text="Back",command=lambda: self.backBtn())
        back_btn.grid(column=0, row=2,columnspan=1, sticky='w')


    def submitBtn(self):
        try:
            # Get user input
            rating = float(self.rating_dropdown.get())
            comment = self.comment_text.get("1.0", "end").strip()

            if not comment:
                comment = None

            # Save to database
            conn = sqlite3.connect("academia.db")
            conn.execute(
                "DELETE FROM Rates WHERE ISBN = ? AND student_id = ?",
                (self.book_item, self.member_id)
            )
            conn.execute(
                "INSERT INTO Rates (ISBN, student_id, comment, grade) VALUES (?, ?, ?, ?)",
                (self.book_item, self.member_id, comment, rating)
            )
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Your rating and comment have been submitted!")
            self.rating_dropdown.set("")
            self.comment_text.delete("1.0", tk.END)
        except ValueError:
            messagebox.showerror("Invalid Input")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


    def backBtn(self):
        self.master.destroy()