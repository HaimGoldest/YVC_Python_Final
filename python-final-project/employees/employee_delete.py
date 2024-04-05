import tkinter as tk
from tkinter import messagebox

import database_manager


class DeleteEmployeeWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.db_manager = database_manager.DatabaseManager()

        self.title("Delete Employee")
        self.geometry("350x150")

        # Label for employee ID entry
        self.employee_id_label = tk.Label(self, text="Enter Employee ID (will be permanently deleted):")
        self.employee_id_label.pack(padx=10, pady=10)

        # Entry field for employee ID
        self.employee_id_entry = tk.Entry(self)
        self.employee_id_entry.pack(padx=10, pady=5)

        # Button frame
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(padx=10, pady=10)

        # Delete button
        self.delete_button = tk.Button(self.button_frame, text="Delete", command=self.delete_employee)
        self.delete_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Cancel button
        self.cancel_button = tk.Button(self.button_frame, text="Cancel", command=self.destroy)
        self.cancel_button.pack(side=tk.RIGHT, padx=10, pady=5)

    def delete_employee(self):
        employee_id = self.employee_id_entry.get()

        if not employee_id:  # Check if employee ID is empty
            messagebox.showerror("Error", "Please enter a employee ID to delete.")
            return  # Exit the function if no employee ID

        try:
            self.db_manager.delete_from_table("employees", f"EmployeeId = {employee_id}")
            messagebox.showinfo("Success", "Employee deleted successfully!")
            self.destroy()  # Close the window
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while deleting the employee: {str(e)}")
            self.destroy()  # Close the window


