import tkinter as tk
from tkinter import ttk, messagebox
import datetime

import database_manager


class LoansReportByDateWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.db_manager = database_manager.DatabaseManager()

        self.title("Loans Report by Date")

        # Date selection frame
        self.date_frame = tk.Frame(self)
        self.date_frame.pack(padx=10, pady=10)

        # Date label
        self.date_label = tk.Label(self.date_frame, text="Select Date:")
        self.date_label.pack(side=tk.LEFT)

        # Date entry (default to today)
        self.selected_date = tk.StringVar(self, value=datetime.date.today().strftime("%Y-%m-%d"))
        self.date_entry = tk.Entry(self.date_frame, textvariable=self.selected_date, width=12)
        self.date_entry.pack(side=tk.LEFT, padx=10)

        # Show loans button
        self.show_loans_button = tk.Button(self.date_frame, text="Show Loans", command=self.get_and_show_loans)
        self.show_loans_button.pack(side=tk.LEFT)

        # Treeview widget for displaying loans
        self.loans_table = ttk.Treeview(self, columns=("LoanID", "MemberID", "Member Name", "BookID", "Book Title",
                                                       "Book Status", "Loan Date", "Due Date", "Return Date"),
                                        show="headings")
        self.loans_table.heading("LoanID", text="Loan ID")
        self.loans_table.heading("MemberID", text="Member ID")
        self.loans_table.heading("Member Name", text="Member Name")
        self.loans_table.heading("BookID", text="Book ID")
        self.loans_table.heading("Book Title", text="Book Title")
        self.loans_table.heading("Book Status", text="Book Status")
        self.loans_table.heading("Loan Date", text="Loan Date")
        self.loans_table.heading("Due Date", text="Due Date")
        self.loans_table.heading("Return Date", text="Return Date")

        # Set column widths (adjust pixel values as needed)
        self.loans_table.column("#0", width=0)  # Hide the first empty column
        self.loans_table.column("LoanID", width=100)
        self.loans_table.column("MemberID", width=100)
        self.loans_table.column("Member Name", width=150)
        self.loans_table.column("BookID", width=100)
        self.loans_table.column("Book Title", width=150)
        self.loans_table.column("Book Status", width=150)
        self.loans_table.column("Loan Date", width=150)
        self.loans_table.column("Due Date", width=150)
        self.loans_table.column("Return Date", width=150)

        self.loans_table.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Close button
        self.close_button = tk.Button(self, text="Close", command=self.destroy)
        self.close_button.pack(padx=10, pady=10)

    def get_and_show_loans(self):
        try:
            # Get selected date
            selected_date_str = self.selected_date.get()

            # Validate date format (YYYY-MM-DD)
            datetime.datetime.strptime(selected_date_str, "%Y-%m-%d")  # Raise ValueError on invalid format

            # Build the query with a filter on LoanDate
            query = 'SELECT loans.LoanID, loans.MemberID, members.Name AS MemberName, loans.BookID, ' \
                    'books.Title AS BookTitle, books.Status AS BookStatus, loans.LoanDate, loans.DueDate, ' \
                    'loans.ReturnDate\n' \
                    'FROM loans\n' \
                    'JOIN books ON loans.BookID = books.BookID\n' \
                    'JOIN members ON loans.MemberID = members.MemberID\n' \
                    f"WHERE loans.LoanDate = '{selected_date_str}';"

            # Execute query with the selected date as a parameter
            loans_data = self.db_manager.execute_query(query)

            # Clear the Treeview before filling with new data
            self.loans_table.delete(*self.loans_table.get_children())

            # Fill the Treeview with loans data (if any)
            self.fill_treeview(loans_data)

        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter a valid date in YYYY-MM-DD format.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to retrieve loans: {str(e)}")

    def fill_treeview(self, loans_data):
        if not loans_data:
            messagebox.showerror("Info", "No loans found for selected date!")
            return

        try:
            for loan in loans_data:
                loan_id, member_id, member_name, book_id, book_title, book_status, loan_date, due_date, return_date = loan
                data = (
                    loan_id, member_id, member_name, book_id, book_title, book_status, loan_date, due_date, return_date)
                self.loans_table.insert("", tk.END, values=data)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to display loans: {str(e)}")
