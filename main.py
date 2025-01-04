import tkinter as tk 
from login_page import LoginFrame

class academia(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("academia")
        self.configure(bg='#eaddc0')
        self.geometry("750x750")
        login_frame=LoginFrame(self)
        login_frame.pack()


app=academia()

app.mainloop()