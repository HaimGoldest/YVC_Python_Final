import tkinter as tk
from tkinter import messagebox
import datetime
import re
import database_manager


class AddMemberWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.db_manager = database_manager.DatabaseManager()

        self.title("Add Member")
        self.geometry("350x250")

        # Labels for input fields
        name_label = tk.Label(self, text="Name:")
        name_label.grid(row=0, column=0, padx=10, pady=5)
        email_label = tk.Label(self, text="Email:")
        email_label.grid(row=1, column=0, padx=10, pady=5)
        phone_label = tk.Label(self, text="Phone:")
        phone_label.grid(row=2, column=0, padx=10, pady=5)

        # Entry fields
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)
        self.email_entry = tk.Entry(self)
        self.email_entry.grid(row=1, column=1, padx=10, pady=5)
        self.phone_entry = tk.Entry(self)
        self.phone_entry.grid(row=2, column=1, padx=10, pady=5)

        # Buttons
        self.add_member_button = tk.Button(self, text="Add Member", command=self.add_member, state=tk.DISABLED)
        self.add_member_button.grid(row=3, column=0, columnspan=1, padx=10, pady=10)
        self.cancel_button = tk.Button(self, text="Cancel", command=self.destroy)
        self.cancel_button.grid(row=3, column=1, columnspan=1, padx=10, pady=10)

        # Bind validation to entry fields
        self.name_entry.bind("<KeyRelease>", self.validate_fields)
        self.email_entry.bind("<KeyRelease>", self.validate_fields)
        self.phone_entry.bind("<KeyRelease>", self.validate_fields)

    def validate_fields(self, event):
        # Check if all entry fields are filled
        all_fields_filled = (
                self.name_entry.get() and
                self.email_entry.get() and
                self.phone_entry.get()
        )

        # Update button state and display email validation message
        if all_fields_filled:
            self.add_member_button.config(state=tk.NORMAL)
            self.email_entry.config(highlightbackground="white")  # Clear any previous error highlight
        else:
            self.add_member_button.config(state=tk.DISABLED)
            if not all_fields_filled:
                self.email_entry.config(highlightbackground="red")  # Highlight for missing field

    def add_member(self):
        try:
            # Get member details from entry fields
            name = self.name_entry.get()
            email = self.email_entry.get()
            phone = self.phone_entry.get()

            # Validate email format
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):  # Basic email format check
                messagebox.showerror("Invalid email", "Please enter a valid email address.")
                return  # Exit the function if email is invalid

            # Get current date in YYYY-MM-DD format
            today = datetime.date.today().strftime('%Y-%m-%d')

            # Create a dictionary with member details (including current date)
            member_data = {
                "Name": name,
                "Email": email,
                "Phone": phone,
                "MembershipStartDate": today
            }

            # add the member
            self.db_manager.add_to_table("members", member_data)  # Pass dictionary instead of string

            messagebox.showinfo("Success", "Member added successfully!")
            # Clear entry fields after successful addition
            self.name_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
            self.phone_entry.delete(0, tk.END)
        except Exception as e:  # Catch any database-related errors
            messagebox.showerror("Error", "Failed to add member: {}".format(str(e)))
