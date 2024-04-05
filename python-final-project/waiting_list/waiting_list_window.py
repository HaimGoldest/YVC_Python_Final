import tkinter as tk

from static_models.waiting_list_model import WaitingListModel

from waiting_list import waiting_list_show_unavailable_books, waiting_new, waiting_list_by_book


class WaitingListWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)  # Inherit from Toplevel for a new window
        self.title("Loans Waiting List")
        self.geometry("400x300")
        self.waiting_list = WaitingListModel()

        # Create header frame
        header_frame = tk.Frame(self, bg="lightblue", height=50)
        header_frame.pack(fill=tk.X)

        # Create header label
        header_label = tk.Label(header_frame, text="Loans Management", font=("Arial", 18, "bold"))
        header_label.pack()

        # Create button frame
        button_frame = tk.Frame(self)
        button_frame.pack(padx=10, pady=10)

        # Create buttons with vertical layout
        button_list = ["Show Unavailable Books", "Add Member To Waiting List", "Show Waiting Members By Book", "Close"]
        for button_text in button_list:
            button = tk.Button(button_frame, text=button_text, command=lambda b=button_text: self.button_clicked(b))
            button.pack(fill=tk.X, pady=5)

    def button_clicked(self, button_text):
        if button_text.endswith("Books"):
            waiting_list_show_unavailable_books.WaitingListShowUnavailableBooksWindow(self)
        elif button_text.endswith("List"):
            waiting_new.AddWaitingMemberWindow(self)
        elif button_text.endswith("Book"):
            waiting_list_by_book.BookWaitingListWindow(self)
        elif button_text.startswith("Close"):
            self.destroy()
