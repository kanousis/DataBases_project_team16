import tkinter as tk
from PIL import ImageTk, Image
import sqlite3

class ProfileFrame(tk.Frame):
    def __init__(self,master,member_id,**kwargs):
        super().__init__(master,bg='#eaddc0', **kwargs)
        self.member_id=member_id
        self.master=master
        self.master.geometry("400x300")
        self.pack()
        self.create_content()
        
    
    def create_content(self):
        color1 = '#eaddc0'
        color2 = '#eaddc0'
        west1_frame = tk.Frame(self, bg=color1)
        west1_frame.grid(column=0,row=0,columnspan=4)
        
        west2_frame = tk.Frame(self, bg=color2)
        west2_frame.grid(column=0,row=2)

        east_frame = tk.Frame(self, bg=color1)
        east_frame.grid(column=3,row=2,rowspan=3)
        
        
        self.conn=sqlite3.connect("academia.db")
        self.cursor=self.conn.execute("SELECT M.member_id, M.first_name, M.last_name, M.street, M.number, M.PC, M.email, M.telephone\
                                       FROM MEMBER AS M\
                                      WHERE M.member_id=?",(self.member_id,))
        data=self.cursor.fetchall() 
        

        profil_info_label=tk.Label(west1_frame, text="PROFILE INFO",bg=color1,fg='black',font=('Calibri', 22, 'bold'))
        id_label=tk.Label(west1_frame, text=data[0][0],bg=color1,fg='black',font=('Calibri', 18, 'bold'))

        fname="Όνομα: "+data[0][1]
        lname="Επίθετο: "+data[0][2]
        phone="Τηλ: "+str(data[0][7])
        email="Email: "+data[0][6]
        member_id="ΑΜ: "+str(data[0][0])
        address="Διεύθυνση: "+str(data[0][3])+ " "+ str(data[0][4])+ " / "+ str(data[0][5])
        
        
        fname_label=tk.Label(west2_frame, text=fname,bg=color2,fg='black',font=('Calibri', 13, 'bold'))
        lname_label=tk.Label(west2_frame, text=lname,bg=color2,fg='black',font=('Calibri', 13, 'bold'))
        phone_label=tk.Label(west2_frame, text=phone,bg=color2,fg='black',font=('Calibri', 13, 'bold'))
        email_label=tk.Label(west2_frame, text=email,bg=color2,fg='black',font=('Calibri', 13, 'bold'))
        member_id_label=tk.Label(west2_frame, text=member_id,bg=color2,fg='black',font=('Calibri', 13, 'bold'))
        address_label=tk.Label(west2_frame,text=address,bg=color2,fg='black',font=('Calibri',13,'bold'))
        credits_label=tk.Label(west2_frame, text=credits,bg=color2,fg='black',font=('Calibri', 13, 'bold'))
        
        back_btn = tk.Button(east_frame,text="Back",command=lambda: self.back(self.member_id),font=('Calibri', 13, 'bold'))
        back_btn.grid(row=3, column=0, pady=5)
        #WEST 2
        fname_label.grid(column=0,row=1)
        lname_label.grid(column=0,row=2)
        member_id_label.grid(column=0,row=3)
        credits_label.grid(column=0,row=4)
        phone_label.grid(column=0,row=5)
        email_label.grid(column=0,row=6)
        address_label.grid(column=0,row=7)

        
        edit_picture = Image.open("./media/edit.png")
        edit_picture = edit_picture.resize((20,20))
        edit_pic = ImageTk.PhotoImage(edit_picture)
        
        edit_btn=tk.Button(east_frame,text="Edit your profile", compound='right', command=lambda: self.edit(self.member_id), font=('Calibri', 13, 'bold'))
        
        
        #WEST 1
        profil_info_label.grid(column=1,row=0, padx=5, columnspan=3)
    
        
        #RIGHT
        edit_btn.grid(row=0, column=0, pady=5)
        
        self.columnconfigure(5, weight=1)
        self.rowconfigure(2, weight=1)
        

            
    def edit(self,member_id):
        from edit_data_prof import EditdataFrame
        self.destroy()
        edit_frame=EditdataFrame(self.master,member_id=self.member_id)
        edit_frame.pack()
        

    def back(self,member_id):
        from home_page_prof import WelcomeFrame
        self.destroy()
        purchase_frame=WelcomeFrame(self.master, member_id=member_id)
        purchase_frame.pack()
