import tkinter as tk
from tkinter import ttk
import sqlite3

class MyBooksFrame(tk.Frame):
    def __init__(self, master, member_id, **kwargs):
        super().__init__(master,bg='#eaddc0',**kwargs)
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight() 
        w= 900
        h = 450
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.member_id=member_id
        self.counter=0
        self.pack()
        self.create_content()

    def create_content(self):
        color1 = '#eaddc0'
        color2 = '#eaddc0'

        conn=sqlite3.connect("academia.db")

        my_books = tk.Frame(self,bg=color1, padx=40)

        my_books.grid(column=0, row=1)
        my_books_label = tk.Label(my_books, text = "My Book Library",bg='#eaddc0',fg='black',font=45)
        my_books_label.config(font=("Calibri", 42, 'bold'))
        my_books_label.grid(column=0, row=0)

        back_btn=tk.Button(self,text="Back" ,font=('Calibri', 13, 'bold'), height=2, width =5,\
            command=lambda: self.back(self.member_id))
        back_btn.grid(column = 0, row = 3,columnspan=1)


        if(self.counter==0):
            self.fill_shed(my_books)

        

    def fill_shed(self,my_books):
        self.counter=self.counter+1
        conn=sqlite3.connect("academia.db")

        self.cursor=conn.execute("SELECT C.ISBN, B.title\
                                  FROM APPLICATION AS A\
                                  INNER JOIN STUDENT AS S ON A.student_id = S.student_id\
                                  INNER JOIN Consists_Of AS C ON A.application_id = C.application_id\
                                  INNER JOIN BOOK AS B ON C.ISBN = B.ISBN\
                                  WHERE A.semester < S.current_semester AND S.student_id=?",(self.member_id,))
        
        data1=self.cursor.fetchall()

        self.cursor=conn.execute("SELECT CRB.ISBN, B.title\
                                 FROM RETURN AS R\
                                 INNER JOIN [Contains(RETURN-BOOK)] AS CRB ON R.return_id = CRB.return_id\
                                 INNER JOIN BOOK AS B ON CRB.ISBN = B.ISBN\
                                 WHERE R.student_id=?",(self.member_id,))
        data2=self.cursor.fetchall()
        data = list(set(data1) - set(data2))

        conn.close()

        books=()

        for j in range(len(data)):
            books += (data[j][0]+ '| Title: '+ str(data[j][1]),)\
                    + ('-----------------------------------------------------------------------------------------------------------',)
            
        books_var= tk.Variable(value=books)

        books_listbox = tk.Listbox(
            my_books,
            listvariable=books_var,
            height=20,
            width=80,
            selectmode=tk.EXTENDED
        )

        books_listbox.grid(row=1,column=0)

        scrollbar = tk.Scrollbar(my_books, orient=tk.VERTICAL, command=books_listbox.yview)
        books_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky="ns")

        books_listbox.bind("<<ListboxSelect>>", self.callback)

    
    def back(self,member_id):
        from home_page import WelcomeFrame
        self.destroy()
        purchase_frame=WelcomeFrame(self.master, member_id=member_id)
        purchase_frame.pack()

    def callback(self,event):
        # return
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            data = event.widget.get(index)
            parts=data.split('|')
            conn=sqlite3.connect("academia.db")
            cursor=conn.execute("SELECT ISBN\
                                FROM BOOK\
                                WHERE ISBN=?",(parts[0].strip(),)).fetchall()
            # print(parts[0].strip())
            book_code=cursor[0][0]
            conn.close()
            from book_rating_window import rateWindow
            book_rating_window=rateWindow(self,book_code, member_id=self.member_id)
            return
        else:
            print("nothing")

