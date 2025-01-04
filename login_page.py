import tkinter as tk
from tkinter import messagebox
import sqlite3

class LoginFrame(tk.Frame):
    def __init__(self,master=None,**kwargs):
        super().__init__(master,bg='#eaddc0',**kwargs)
        self.master=master
        self.master.title("academia")
        w= 350
        h = 400
        ws = self.master.winfo_screenwidth() # width of the screen
        hs = self.master.winfo_screenheight() # height of the screen
        x = (ws/2) - (5*w/3)
        y = h/4
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.pack()
        self.create_content()

    
    def create_content(self):
        login_label=tk.Label(self, text="Login",bg='#eaddc0',fg='black',font=30)
        academia_label=tk.Label(self,text='academia',bg='#eaddc0',fg='black',font=30)
        member_id_label=tk.Label(self, text="Member_ID",bg='#eaddc0',fg='black',font=30)
        self.member_id_entry=tk.Entry(self)
        password_label=tk.Label(self, text="Password",bg='#eaddc0',fg='black',font=30)
        self.password_entry=tk.Entry(self,show="*")
        login_btn=tk.Button(self,text="LOGIN",command=lambda: self.login(None))
        var=tk.IntVar()
        show_pass=tk.Checkbutton(self,text="Show Password",variable=var,onvalue=1,offvalue=0,bg='#eaddc0',fg='black',font=5,command=lambda: self.showpassword(var.get()),selectcolor='white')
        login_label.grid(row=1,column=0,columnspan=2,sticky="news",pady=10)
        member_id_label.grid(row=2,column=0,padx=5)
        self.member_id_entry.grid(row=2,column=1,pady=20)
        password_label.grid(row=3,column=0,padx=5)
        self.password_entry.grid(row=3,column=1,pady=20)
        login_btn.grid(row=5,column=0,columnspan=2,pady=10)
        show_pass.grid(row=4,column=0,columnspan=2)
        self.master.bind("<Return>",self.login)

    def login(self,event):
        #sql code here for validation
        member_id=self.member_id_entry.get()
        password=self.password_entry.get()
        self.conn=sqlite3.connect('academia.db')
        self.cursor=self.conn.execute("SELECT member_id,password FROM MEMBER WHERE member_id=?",(member_id,))
        data=self.cursor.fetchall()    
        if (data==[]):
            messagebox.showerror("User Not Found", "Check your member_id, or create an account")

        # self.conn.close()
        
        if int(member_id) == data[0][0] and password == data[0][1]:
            self.cursor = self.conn.execute("SELECT professor_id FROM PROFESSOR WHERE professor_id=?", (member_id,))
            professor_data = self.cursor.fetchall()
            self.cursor = self.conn.execute("SELECT student_id FROM STUDENT WHERE student_id=?", (member_id,))
            student_data = self.cursor.fetchall()

            self.conn.close()

            if professor_data:
                user_type = "Professor"
            elif student_data:
                user_type = "Student"
            else:
                user_type = "Unknown"

            if (user_type=="Student"):
                # Destroy current frame and show welcome frame fow Student
                self.destroy()
            
                from home_page import WelcomeFrame
                welcome_frame = WelcomeFrame(self.master,member_id=member_id)
                welcome_frame.pack()

            elif (user_type=="Professor"):
                # Destroy current frame and show welcome frame for Professor
                self.destroy()
            
                from home_page_prof import WelcomeFrame
                welcome_frame = WelcomeFrame(self.master,member_id=member_id)
                welcome_frame.pack()    
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

        

    def showpassword(self,state):
        if state==0:
            self.password_entry.configure(show="*")
        else:
            self.password_entry.configure(show="")
