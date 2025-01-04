import tkinter as tk


class rateWindow(tk.Toplevel):
    def __init__(self, master, book_item, member_id):
        self.master=master
        super().__init__(self.master)
        self.title("Rate Book")
        self.member_id=member_id
        self.book_item=book_item
        self.configure(bg='#eaddc0')
        self.geometry("500x500")
        self.focus()
        self.startframe=tk.Frame(self, bg='#eaddc0')
        self.create_content()


    def create_content(self):
        from book_rating_frame import RatingFrame
        bookframe=RatingFrame(self,book_item=self.book_item, member_id=self.member_id)
        bookframe.grid()
        return
        
    def backBtn(self):
        self.destroy()
        return





