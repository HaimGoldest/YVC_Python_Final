import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import database_manager


class NewLoanWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.db_manager = database_manager.DatabaseManager()

        self.title("Add New Loan")
        self.geometry("300x200")

        # Labels for input fields
        book_id_label = tk.Label(self, text="Book ID:")
        book_id_label.grid(row=0, column=0, padx=10, pady=5)
        member_id_label = tk.Label(self, text="Member ID:")
        member_id_label.grid(row=1, column=0, padx=10, pady=5)

        # Entry fields
        self.book_id_entry = tk.Entry(self)
        self.book_id_entry.grid(row=0, column=1, padx=10, pady=5)
        self.member_id_entry = tk.Entry(self)
        self.member_id_entry.grid(row=1, column=1, padx=10, pady=5)

        # Buttons
        self.add_loan_button = tk.Button(self, text="Add Loan", command=self.add_loan, state=tk.DISABLED)
        self.add_loan_button.grid(row=5, column=0, columnspan=1, padx=10, pady=10)
        self.cancel_button = tk.Button(self, text="Cancel", command=self.destroy)
        self.cancel_button.grid(row=5, column=1, columnspan=1, padx=10, pady=10)

        # Bind validation to entry fields
        self.book_id_entry.bind("<KeyRelease>", self.validate_fields)
        self.member_id_entry.bind("<KeyRelease>", self.validate_fields)

    def validate_fields(self, event):
        # Check if all entry fields are filled
        all_fields_filled = (
                self.book_id_entry.get() and
                self.member_id_entry.get()
        )

        # Enable or disable the "Add Loan" button based on validation
        self.add_loan_button.config(state=tk.NORMAL if all_fields_filled else tk.DISABLED)

    def add_loan(self):
        try:
            # Get loan details from entry fields
            book_id = self.book_id_entry.get()
            member_id = self.member_id_entry.get()

            # Check book status before adding loan
            book_status = self.get_book_status(book_id)

            if book_status != "Available":
                messagebox.showwarning("Warning", "This book is not available!")
                return

            # Change book status to 'In Use'
            self.update_book_status(book_id)

            today = datetime.today()
            due_date = today + timedelta(days=7)

            # Format dates as strings
            today_str = today.strftime('%Y-%m-%d')
            due_date_str = due_date.strftime('%Y-%m-%d')

            # Create loan data dictionary
            loan_data = {
                "BookID": book_id,
                "MemberID": member_id,
                "LoanDate": today_str,
                "DueDate": due_date_str,
            }

            # Add loan to database
            self.db_manager.add_to_table("loans", loan_data)

            messagebox.showinfo("Success", "Loan added successfully!")
            self.destroy()  # Close the window
        except Exception as e:  # Catch any database-related errors
            messagebox.showerror("Error", "Failed to add loan: {}".format(str(e)))

    def get_book_status(self, book_id):
        condition = f"BookID LIKE {book_id}"
        return self.db_manager.read_from_table("books", "Status", condition)[0][0]

    def update_book_status(self, book_id):
        values = {
            "Status": 'In Use',
        }
        condition = f"BookID LIKE {book_id}"
        self.db_manager.update_table("books", values, condition)

