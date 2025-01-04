import tkinter as tk
from tkinter import ttk
import sqlite3

class MyCoursesFrame(tk.Frame):
    def __init__(self, master, member_id, **kwargs):
        super().__init__(master,bg='#eaddc0',**kwargs)
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight() 
        w= 900
        h = 350
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.member_id=member_id
        self.curent_academic_year="2024-2025"
        self.counter=0
        self.pack()
        self.create_content()


    def create_content(self):
        color1 = '#eaddc0'
        color2 = '#eaddc0'

        my_courses = tk.Frame(self,bg=color1, padx=40)

        my_courses.grid(column=0, row=1)
        my_courses_label = tk.Label(my_courses, text = "My Courses",bg='#eaddc0',fg='black',font=45)
        my_courses_label.config(font=("Arial", 42, 'bold'))
        my_courses_label.grid(column=0, row=0)

        back_btn=tk.Button(self,text="Back" ,font=('Arial', 13, 'bold'), height=2, width =5,\
            command=lambda: self.back(self.member_id))
        back_btn.grid(column = 0, row = 3,columnspan=1)


        if(self.counter==0):
            self.fill_shed(my_courses)


    def fill_shed(self,my_courses):
        self.counter=self.counter+1
        conn=sqlite3.connect("academia.db")

        self.cursor=conn.execute("SELECT CT.course_id, C.title, CT.semester\
                                FROM COURSE_TEACHING AS CT JOIN COURSE AS C ON CT.course_id=C.course_id\
                                WHERE CT.professor_id=? AND CT.academic_year=?",(self.member_id,self.curent_academic_year))
                             
        data=self.cursor.fetchall()

        conn.close()

        books=()

        for j in range(len(data)):
            books += (data[j][0]+ '| Course Title: '+ str(data[j][1])+ '| Semester: '+ str(data[j][2]),)\
                    + ('-------------------------------------------------------------------------------------------------------------------',)
            
        books_var= tk.Variable(value=books)

        books_listbox = tk.Listbox(
            my_courses,
            listvariable=books_var,
            height=10,
            width=80,
            selectmode=tk.EXTENDED
        )

        books_listbox.grid(row=1,column=0)

        scrollbar = tk.Scrollbar(my_courses, orient=tk.VERTICAL, command=books_listbox.yview)
        books_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky="ns")

        books_listbox.bind("<<ListboxSelect>>", self.callback)


    def back(self,member_id):
        from home_page_prof import WelcomeFrame
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
            cursor=conn.execute("SELECT course_id\
                                FROM COURSE\
                                WHERE course_id=?",(parts[0].strip(),)).fetchall()
            course_code=cursor[0][0]
            conn.close()
            from choose_books_for_course_window import chooseBookWindow
            choose_books_for_course_window=chooseBookWindow(self,course_code, member_id=self.member_id, semester=parts[2].strip(), curent_academic_year = self.curent_academic_year)
            return
        else:
            print("nothing")