import tkinter as tk

from loans import loan_new, loan_returned, loan_show_all


class LoansManagementWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)  # Inherit from Toplevel for a new window
        self.title("Loans Management")
        self.geometry("400x300")

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
        button_list = ["New Loan", "Book Returned", "Show All", "Close"]
        for button_text in button_list:
            button = tk.Button(button_frame, text=button_text, command=lambda b=button_text: self.button_clicked(b))
            button.pack(fill=tk.X, pady=5)

    def button_clicked(self, button_text):
        if button_text.endswith("Loan"):
            loan_new.NewLoanWindow(self)  # Create NewLoanWindow
        elif button_text.endswith("Returned"):
            loan_returned.LoanReturnedWindow(self)  # Create LoanReturnedWindow
        elif button_text.endswith("All"):
            loan_show_all.ShowAllLoansWindow(self)  # Create ShowAllLoansWindow
        elif button_text.startswith("Close"):
            self.destroy()  # Close the window
