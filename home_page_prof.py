import tkinter as tk
import sqlite3
from PIL import ImageTk, Image
import tkinter.font as tkFont

class WelcomeFrame(tk.Frame):
    def __init__(self, master, member_id, **kwargs):
        super().__init__(master,bg='#eaddc0',**kwargs)
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        w= 700
        h = 300
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.member_id=member_id
        self.pack()
        self.create_content()

    def create_content(self):
        welcome = tkFont.Font(family="Helvetica",size=30,weight="bold")
        prof = tkFont.Font(family="Helvetica",size=10,weight="bold")
        rest = tkFont.Font(family="Helvetica",size=15,weight="bold")

        self.conn=sqlite3.connect("academia.db")
        self.cursor=self.conn.execute("SELECT first_name\
                                       FROM MEMBER\
                                      WHERE member_id=?",(self.member_id,))
        data=self.cursor.fetchall() 
        welcomemsg="Welcome to academia"
        self.conn.close()
        label = tk.Label(self, text=welcomemsg, font=welcome, bg='#eaddc0')
        
        
        prof_picture = Image.open("./media/prof.jpg")
        prof_picture = prof_picture.resize((80,80))
        prof_pic = ImageTk.PhotoImage(prof_picture)  

        prof_pic_label = tk.Label(self,image=prof_pic)
        prof_pic_label.image = prof_pic

        log_picture = Image.open("./media/logout.png")
        log_picture = log_picture.resize((50,50))
        log_pic = ImageTk.PhotoImage(log_picture)  

        log_pic_label = tk.Label(self,image=log_pic)
        log_pic_label.image = log_pic

        application_picture = Image.open("./media/application.jpg")
        application_picture = application_picture.resize((50,50))
        application_pic = ImageTk.PhotoImage(application_picture)  

        application_pic_label = tk.Label(self,image=application_pic)
        application_pic_label.image = application_pic


        logout_button = tk.Button(self, text="Logout",image=log_pic,command=self.logout)
        choose_book_button = tk.Button(self, text="CHOOSE BOOK FOR COURSE",image=application_pic, command=self.choose_book, width=350, height=120, compound='left', font=rest)
        profile_button = tk.Button(self,image=prof_pic, command=self.myprofile, text=data[0][0], compound='right', padx=5, font=prof)

        label.grid(column=1, columnspan=5,row=0, rowspan=3, pady=20, sticky='E')

        choose_book_button.grid(column=0,row=3, columnspan=4, rowspan=2, padx=10, pady=10)

        logout_button.grid(column=8,row=0)
        profile_button.grid(column=7,row=0, padx=20,  pady=10)

    def logout(self):
        # Destroy current frame and show login frame
        self.destroy()
        from login_page import LoginFrame
        login_frame=LoginFrame(self.master)
        login_frame.pack()
        
    def myprofile(self):
        from profile_page_prof import ProfileFrame
        if hasattr(self,'myprofile_frame'):
            return
        self.destroy()
        self.myprofile_frame=ProfileFrame(self.master,member_id=self.member_id)
        self.myprofile_frame.pack()
   
        
    def choose_book(self):
        from courses_to_teach import MyCoursesFrame
        if hasattr(self, 'choose_book_frame'):
            return
        self.destroy()
        self.application_frame = MyCoursesFrame(self.master, member_id=self.member_id)
        self.application_frame.pack()