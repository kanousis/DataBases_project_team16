import tkinter as tk


class chooseBookWindow(tk.Toplevel):
    def __init__(self, master, course_id, member_id, semester, curent_academic_year):
        self.master=master
        super().__init__(self.master)
        self.title("Choose Books")
        self.member_id=member_id
        self.course_id=course_id
        self.semester=semester
        self.curent_academic_year=curent_academic_year
        self.master=master
        self.geometry("800x500")
        self.create_content()


    def create_content(self):
        from choose_books_for_course_frame import chooseBookFrame
        courseframe=chooseBookFrame(self,course_id=self.course_id, member_id=self.member_id, semester=self.semester, curent_academic_year=self.curent_academic_year)
        courseframe.grid()
        return
        
    def backBtn(self):
        self.destroy()
        return
