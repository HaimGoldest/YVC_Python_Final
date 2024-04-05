import tkinter as tk
from tkinter import messagebox
import database_manager


class LoginWindow(tk.Tk):
    def __init__(self, user_data):
        super().__init__()
        self.db_manager = database_manager.DatabaseManager()
        self.user_data = user_data

        self.title("Login")
        self.geometry("400x150")

        # Email and password labels and entries
        email_label = tk.Label(self, text="Email:")
        email_label.grid(row=0, column=0, padx=10, pady=5)
        self.email_entry = tk.Entry(self, width=40)
        self.email_entry.grid(row=0, column=1, padx=10, pady=5)

        password_label = tk.Label(self, text="Password:")
        password_label.grid(row=1, column=0, padx=10, pady=5)
        self.password_entry = tk.Entry(self, show="*", width=40)  # Hide password characters
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        # Login button
        self.login_button = tk.Button(self, text="Login", command=self.login)
        self.login_button.grid(row=2, columnspan=2, padx=10, pady=10)

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        # Validate empty fields
        if not email or not password:
            messagebox.showerror("Error", "Please enter email and password!")
            return

        if self.is_admin_user(email, password):
            self.destroy()  # Close the login window
            return

        try:
            # Get all employees
            employees = self.db_manager.execute_query("SELECT * FROM employees")

            # Check if user credentials match an employee in the database
            for employee in employees:
                emp_name, emp_email, emp_password, emp_type = employee[1], employee[2], employee[3], employee[5]
                if email == emp_email and password == emp_password:
                    self.user_data.set_user_data(emp_name, emp_type)
                    self.destroy()  # Close the login window
                    return

            # Login failed (no matching credentials)
            messagebox.showerror("Error", "Invalid email or password!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to login: {str(e)}")

    def is_admin_user(self, email, password):
        admin_username = 'admin'
        admin_password = '1234'

        if email == admin_username and password == admin_password:
            self.user_data.set_user_data(admin_username, 'manager')
            return True

        return False



