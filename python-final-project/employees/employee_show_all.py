import tkinter as tk
from tkinter import ttk

import database_manager


class ShowAllEmployeesWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.db_manager = database_manager.DatabaseManager()

        self.title("All Employees")

        # Treeview widget for displaying employees
        self.employees_table = ttk.Treeview(self, columns=("EmployeeId", "Name", "Email", "Phone", "EmployeeType"),
                                            show="headings")
        self.employees_table.heading("EmployeeId", text="Employee ID")
        self.employees_table.heading("Name", text="Name")
        self.employees_table.heading("Email", text="Email")
        self.employees_table.heading("Phone", text="Phone")
        self.employees_table.heading("EmployeeType", text="Role")
        self.employees_table.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Get all employees
        self.employees_data = self.db_manager.read_from_table("employees", "EmployeeId, Name, Email, Phone, "
                                                                           "EmployeeType")

        # Fill the Treeview with employees data
        for employee in self.employees_data:
            self.employees_table.insert("", tk.END, values=employee)

        # Close button
        self.close_button = tk.Button(self, text="Close", command=self.destroy)
        self.close_button.pack(padx=10, pady=10)
