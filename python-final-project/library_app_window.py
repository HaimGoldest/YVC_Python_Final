import tkinter as tk

from books import books_management_window
from employees import employees_management_window
from loans import loans_management_window
from members import members_management_window
from static_models.user_model import UserDataModel
from reports import reports_management_window
from waiting_list import waiting_list_window


class LibraryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Library Management")
        self.geometry("400x500")

        # Create header frame
        header_frame = tk.Frame(self, bg="lightblue", height=50)
        header_frame.pack(fill=tk.X)  # Fill horizontally

        # Create hello user label
        username = UserDataModel.get_user_name()
        hello_user_label = tk.Label(self, text=f"User: {username}", font=("Arial", 16))
        hello_user_label.pack(pady=10)  # Add padding

        # Create header label
        header_label = tk.Label(header_frame, text="Library Management", font=("Arial", 18, "bold"))
        header_label.pack()

        # Create button frame
        button_frame = tk.Frame(self)
        button_frame.pack(padx=10, pady=10)

        # Create buttons with vertical layout
        button_list = ["Book Management", "Members Management", "Loans Management", "Waiting List",
                       "Reports and Statistics", "Employees Management", "Close"]
        for button_text in button_list:
            button = tk.Button(button_frame, text=button_text, command=lambda b=button_text: self.button_clicked(b))
            button.pack(fill=tk.X, pady=5)

    def button_clicked(self, button_text):
        if button_text.startswith("Book"):
            books_management_window.BooksManagementWindow(self)  # Create BookManagementWindow
        if button_text.startswith("Members"):
            members_management_window.MembersManagementWindow(self)  # Create MembersManagementWindow
        if button_text.startswith("Loans"):
            loans_management_window.LoansManagementWindow(self)  # Create LoansManagementWindow
        if button_text.startswith("Waiting"):
            waiting_list_window.WaitingListWindow(self)  # Create WaitingListWindow
        if button_text.startswith("Employees"):
            employees_management_window.EmployeesManagementWindow(self)  # Create EmployeesManagementWindow
        if button_text.startswith("Reports"):
            reports_management_window.ReportsManagementWindow(self)  # Create ReportsManagementWindow
        elif button_text.startswith("Close"):
            self.destroy()  # Close the window
