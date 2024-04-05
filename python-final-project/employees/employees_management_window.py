import tkinter as tk
from tkinter import messagebox

from employees import employee_show_all, employee_add, employee_delete

from static_models.user_model import UserDataModel


class EmployeesManagementWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)  # Inherit from Toplevel for a new window
        self.title("Employees Management")
        self.geometry("400x300")

        # Create header frame
        header_frame = tk.Frame(self, bg="lightblue", height=50)
        header_frame.pack(fill=tk.X)

        # Create header label
        header_label = tk.Label(header_frame, text="Employees Management", font=("Arial", 18, "bold"))
        header_label.pack()

        # Close if the user not a manager
        if self.is_not_manager():
            messagebox.showerror("Unauthorized user", "This page is only for Managers!")
            self.destroy()
            return

        # Create button frame
        button_frame = tk.Frame(self)
        button_frame.pack(padx=10, pady=10)

        # Create buttons with vertical layout
        button_list = ["Show All Employees", "Add Employee", "Delete Employee", "Close"]
        for button_text in button_list:
            button = tk.Button(button_frame, text=button_text, command=lambda b=button_text: self.button_clicked(b))
            button.pack(fill=tk.X, pady=5)

    def button_clicked(self, button_text):
        if button_text.startswith("Add"):
            employee_add.AddEmployeeWindow(self)  # Create AddEmployeeWindow
        elif button_text.startswith("Delete"):
            employee_delete.DeleteEmployeeWindow(self)  # Create DeleteEmployeeWindow
        elif button_text.startswith("Show"):
            employee_show_all.ShowAllEmployeesWindow(self)  # Create ShowAllEmployeesWindow
        elif button_text.startswith("Close"):
            self.destroy()  # Close the window

    @staticmethod
    def is_not_manager():
        return UserDataModel.get_user_type() != 'manager'
