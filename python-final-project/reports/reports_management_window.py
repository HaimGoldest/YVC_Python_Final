import tkinter as tk

from employees import employee_show_all, employee_add, employee_delete
from reports import report_loans_by_date, report_returned_loans, report_popular_books


class ReportsManagementWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)  # Inherit from Toplevel for a new window
        self.title("Reports and Statistics")
        self.geometry("400x300")

        # Create header frame
        header_frame = tk.Frame(self, bg="lightblue", height=50)
        header_frame.pack(fill=tk.X)

        # Create header label
        header_label = tk.Label(header_frame, text="Reports and Statistics", font=("Arial", 18, "bold"))
        header_label.pack()

        # Create button frame
        button_frame = tk.Frame(self)
        button_frame.pack(padx=10, pady=10)

        # Create buttons with vertical layout
        button_list = ["Show Loans By date", "Show returned loans", "Show most popular books", "Close"]
        for button_text in button_list:
            button = tk.Button(button_frame, text=button_text, command=lambda b=button_text: self.button_clicked(b))
            button.pack(fill=tk.X, pady=5)

    def button_clicked(self, button_text):
        if button_text.endswith("date"):
            report_loans_by_date.LoansReportByDateWindow(self)  # Create LoansReportByDateWindow
        elif button_text.endswith("loans"):
            report_returned_loans.ReturnedLoansReportWindow(self)  # Create ReturnedLoansReportWindow
        elif button_text.endswith("books"):
            report_popular_books.PopularBooksReportWindow(self)  # Create PopularBooksReportWindow
        elif button_text.startswith("Close"):
            self.destroy()  # Close the window
