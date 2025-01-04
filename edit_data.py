import tkinter as tk
from tkinter import messagebox
import sqlite3
import tkinter.font as tkFont
import re

class EditdataFrame(tk.Frame):
    def __init__(self,master,member_id,**kwargs):
        super().__init__(master,bg='#eaddc0',**kwargs)
        self.master=master
        self.master.geometry("620x600")
        self.pack(side='left')
        self.member_id=member_id
        self.create_content(self.member_id)
        self.newumember_id=member_id
        
    
    def create_content(self,member_id):
        helv1 = tkFont.Font(family="Helvetica",size=20,weight="bold")
        helv2 = tkFont.Font(family="Helvetica",size=10,weight="bold")
        self.conn=sqlite3.connect("academia.db")

        self.curr=self.conn.execute("SELECT M.member_id, M.first_name, M.last_name, S.department, S.current_semester, S.credits, M.street, M.number, M.PC, M.email, M. telephone\
                                       FROM MEMBER AS M, STUDENT AS S\
                                      WHERE M.member_id=?",(self.member_id,))
        data=self.curr.fetchall()
        self.conn.close()
        register_label=tk.Label(self, text="Edit your account",bg='#eaddc0',fg='black',font=helv1)
        email_label=tk.Label(self, text="Email",bg='#eaddc0',fg='black',font=helv2)
        email_entry=tk.Entry(self)
        email_entry.insert(0,data[0][9])
        oldpass_label=tk.Label(self, text="Old Password",bg='#eaddc0',fg='black',font=helv2)
        old_pass_entry=tk.Entry(self,show="*")
        new_pass_label=tk.Label(self, text="New Password",bg='#eaddc0',fg='black',font=helv2)
        new_pass_entry=tk.Entry(self,show="*")
        new_pass_valid=tk.Entry(self,show="*")
        new_pass_valid_label=tk.Label(self, text="Confirm New Password",bg='#eaddc0',fg='black',font=helv2)
        
        first_name_entry=tk.Entry(self)
        first_name_entry.insert(0,data[0][1])
        first_name_label=tk.Label(self,text="Όνομα",bg='#eaddc0',fg='black',font=helv2)
        
        last_name_entry=tk.Entry(self)
        last_name_entry.insert(0,data[0][2])
        last_name_label=tk.Label(self,text="Επώνυμο",bg='#eaddc0',fg='black',font=helv2)
        
        member_id_entry=tk.Label(self,text=str(data[0][0]),bg='#eaddc0',fg='black',font=helv2)
        member_id_label=tk.Label(self, text="Member_ID",bg='#eaddc0',fg='black',font=helv2)

        semester_entry=tk.Label(self, text=str(data[0][4]),bg='#eaddc0',fg='black',font=helv2)
        semester_label=tk.Label(self, text="Current Semester",bg='#eaddc0',fg='black',font=helv2)

        department_entry=tk.Label(self, text=str(data[0][3]),bg='#eaddc0',fg='black',font=helv2)
        department_label=tk.Label(self, text="Department",bg='#eaddc0',fg='black',font=helv2)

        address = str(data[0][6])+ " "+ str(data[0][7])+ " /"+ str(data[0][8])
        address_entry=tk.Label(self, text=address,bg='#eaddc0',fg='black',font=helv2)
        address_label=tk.Label(self, text="Address",bg='#eaddc0',fg='black',font=helv2)

        phone_entry=tk.Entry(self)
        phone_entry.insert(0,data[0][10]) 
        phone_label=tk.Label(self, text="Phone",bg='#eaddc0',fg='black',font=helv2)
       
        
        save_btn=tk.Button(self,text="Save",font=helv2,command=lambda: self.saveBtn(member_id,email_entry.get(),old_pass_entry.get(),new_pass_valid.get(),new_pass_entry.get(),first_name_entry.get(),last_name_entry.get(),phone_entry.get()))

        var=tk.IntVar()
        show_pass=tk.Checkbutton(self,text="Show Password",variable=var,onvalue=1,offvalue=0,bg='#eaddc0',\
            fg='black',font=helv2,command=lambda: self.showpassword(var.get(),old_pass_entry,new_pass_valid,new_pass_entry))

        first_name_label.grid(row=2,column=0,padx=5)
        first_name_entry.grid(row=2,column=1,pady=10)

        last_name_label.grid(row=3,column=0,padx=5)
        last_name_entry.grid(row=3,column=1,pady=10)

        register_label.grid(row=1,column=0,columnspan=2,sticky="news",pady=10)

        email_label.grid(row=4,column=0,padx=5)
        email_entry.grid(row=4,column=1,pady=10)
        oldpass_label.grid(row=5,column=0,padx=5)
        old_pass_entry.grid(row=5,column=1,pady=10)
        new_pass_label.grid(row=6,column=0,padx=5)
        new_pass_entry.grid(row=6,column=1,pady=10)
        new_pass_valid.grid(row=7,column=1,pady=10)
        new_pass_valid_label.grid(row=7,column=0,padx=5)
        show_pass.grid(row=8,column=1,padx=5)

        member_id_entry.grid(row=2,column=3,pady=10)
        member_id_label.grid(row=2,column=2,padx=5)
        semester_entry.grid(row=3,column=3,pady=10)
        semester_label.grid(row=3,column=2,padx=5)
        department_entry.grid(row=4,column=3,pady=10)
        department_label.grid(row=4,column=2,padx=5)
        address_entry.grid(row=5,column=3,pady=10)
        address_label.grid(row=5,column=2,padx=5)
        phone_entry.grid(row=7,column=3,pady=10)
        phone_label.grid(row=7,column=2,padx=5)
        save_btn.grid(row=10,column=1,columnspan=2,pady=20)

      

        phone_label.grid(row=6,column=2,padx=5)
        phone_entry.grid(row=6,column=3,pady=10)


        back_btn=tk.Button(self,text="Back",command=lambda: self.backBtn(),font=helv2)
        back_btn.grid(column=0,row=10)

    def saveBtn(self,member_id,email,oldpass,newpassvalid,newpass,first_name, last_name, phone):
        self.conn=sqlite3.connect("academia.db")
        self.curr=self.conn.execute("SELECT member_id, password\
                                    FROM MEMBER\
                                    WHERE member_id=?",(member_id,))
        data=self.curr.fetchall()
        member_id=data[0][0]
        password=data[0][1]


        if (oldpass!="" and newpass!="" and newpassvalid!=""):
            if (password==oldpass):
                if(newpass==newpassvalid):
                    self.conn.execute("UPDATE MEMBER\
                                    SET password=?\
                                    WHERE member_id=?",(newpass,member_id,))
                    self.conn.commit()
                else:
                    messagebox.showerror("Change Password Failed", "New Passwords not match")
                    return 0
            else:
                messagebox.showerror("Change Password Failed", "Old Password Not Correct")
                return 0

        if(phone!="" and not len(phone)==10):
            messagebox.showerror("Error", "Invalid Phone Number")
            return
        
        if(phone==""):
            phone=None

        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if(email!="" and not re.match(email_regex,email)):
            messagebox.showerror("Error", "Invalid Email")
            return
        
        else:
            self.conn.execute("UPDATE MEMBER\
                          SET first_name=?,last_name=?, telephone=?, email=?\
                          WHERE member_id=?",(first_name, last_name, phone, email, member_id))

        self.conn.commit()

        self.conn.close()
        messagebox.showinfo("Info Changed","Your info changed successfully")

    def showpassword(self,state,oldpass,newpassvalid,newpass):
        if state==0:
            oldpass.configure(show="*")
            newpassvalid.configure(show="*")
            newpass.configure(show="*")
        else:
            oldpass.configure(show="")
            newpassvalid.configure(show="")
            newpass.configure(show="")
        
    def backBtn(self):
        self.destroy()
        from profile_page import ProfileFrame
        profFrame=ProfileFrame(self.master,member_id=self.member_id)
        profFrame.pack()
            
