import tkinter as tk
from tkinter import messagebox

import datetime

import re

import database_manager


class AddEmployeeWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.db_manager = database_manager.DatabaseManager()

        self.title("Add Employee")
        self.geometry("350x300")

        # Labels for input fields
        name_label = tk.Label(self, text="Name:")
        name_label.grid(row=0, column=0, padx=10, pady=5)
        email_label = tk.Label(self, text="Email:")
        email_label.grid(row=1, column=0, padx=10, pady=5)
        password_label = tk.Label(self, text="Password:")
        password_label.grid(row=2, column=0, padx=10, pady=5)
        phone_label = tk.Label(self, text="Phone:")
        phone_label.grid(row=3, column=0, padx=10, pady=5)

        # Entry fields
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)
        self.email_entry = tk.Entry(self)
        self.email_entry.grid(row=1, column=1, padx=10, pady=5)
        self.password_entry = tk.Entry(self)
        self.password_entry.grid(row=2, column=1, padx=10, pady=5)
        self.phone_entry = tk.Entry(self)
        self.phone_entry.grid(row=3, column=1, padx=10, pady=5)

        # Employee type radio buttons (default worker)
        self.employee_type = tk.StringVar(self, value="worker")  # String variable to store selected type

        worker_radio = tk.Radiobutton(self, text="Worker", variable=self.employee_type, value="worker")
        worker_radio.grid(row=4, column=0, padx=10, pady=5)
        manager_radio = tk.Radiobutton(self, text="Manager", variable=self.employee_type, value="manager")
        manager_radio.grid(row=4, column=1, padx=10, pady=5)

        # Buttons
        self.add_employee_button = tk.Button(self, text="Add Employee", command=self.add_employee, state=tk.DISABLED)
        self.add_employee_button.grid(row=5, column=0, columnspan=1, padx=10, pady=10)
        self.cancel_button = tk.Button(self, text="Cancel", command=self.destroy)
        self.cancel_button.grid(row=5, column=1, columnspan=1, padx=10, pady=10)

        # Bind validation to entry fields
        self.name_entry.bind("<KeyRelease>", self.validate_fields)
        self.email_entry.bind("<KeyRelease>", self.validate_fields)
        self.password_entry.bind("<KeyRelease>", self.validate_fields)
        self.phone_entry.bind("<KeyRelease>", self.validate_fields)

    def validate_fields(self, event):
        # Check if all entry fields are filled
        all_fields_filled = (
                self.name_entry.get() and
                self.email_entry.get() and
                self.password_entry.get() and
                self.phone_entry.get()
        )

        # Update button state and display email validation message
        if all_fields_filled:
            self.add_employee_button.config(state=tk.NORMAL)
            self.email_entry.config(highlightbackground="white")  # Clear any previous error highlight
        else:
            self.add_employee_button.config(state=tk.DISABLED)
            if not all_fields_filled:
                self.email_entry.config(highlightbackground="red")  # Highlight for missing field

    def add_employee(self):
        try:
            # Get employee details from entry fields
            name = self.name_entry.get()
            email = self.email_entry.get()
            password = self.password_entry.get()
            phone = self.phone_entry.get()

            # Validate email format
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):  # Basic email format check
                messagebox.showerror("Invalid email", "Please enter a valid email address.")
                return  # Exit the function if email is invalid

            # Get current date in YYYY-MM-DD format
            today = datetime.date.today().strftime('%Y-%m-%d')

            # Get selected employee type from radio button variable
            employee_type = self.employee_type.get()

            # Create a dictionary with employee details (including current date and type)
            employee_data = {
                "Name": name,
                "Email": email,
                "password": password,
                "Phone": phone,
                "EmployeeType": employee_type
            }

            # Add the employee
            self.db_manager.add_to_table("employees", employee_data)  # Pass dictionary instead of string

            messagebox.showinfo("Success", "Employee added successfully!")
            # Clear entry fields after successful addition
            self.name_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.phone_entry.delete(0, tk.END)
        except Exception as e:  # Catch any database-related errors
            messagebox.showerror("Error", "Failed to add employee: {}".format(str(e)))
