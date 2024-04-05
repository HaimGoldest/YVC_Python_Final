import tkinter as tk
from tkinter import ttk, messagebox

import database_manager


class ShowAllLoansWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.db_manager = database_manager.DatabaseManager()

        self.title("All Loans")

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

        # Get all loans data
        self.loans_data = self.get_all_loans()

        # Fill the Treeview with loans data
        self.fill_treeview()

        # Close button
        self.close_button = tk.Button(self, text="Close", command=self.destroy)
        self.close_button.pack(padx=10, pady=10)

    def get_all_loans(self):
        query = """
            SELECT
                loans.LoanID,
                loans.MemberID,
                members.Name AS MemberName,
                loans.BookID,
                books.Title AS BookTitle,
                books.Status AS BookStatus,
                loans.LoanDate,
                loans.DueDate,
                loans.ReturnDate
            FROM loans
            JOIN books ON loans.BookID = books.BookID
            JOIN members ON loans.MemberID = members.MemberID;
        """
        return self.db_manager.execute_query(query)

    def fill_treeview(self):
        if not self.loans_data:
            self.loans_table.insert("", tk.END, values=("No loans found", "", "", "", "", "", "", "", ""))
            return

        try:
            for loan in self.loans_data[::-1]:  # Iterate in reverse order
                loan_id, member_id, member_name, book_id, book_title, book_status, loan_date, due_date, return_date = loan
                data = (
                    loan_id, member_id, member_name, book_id, book_title, book_status, loan_date, due_date, return_date)
                self.loans_table.insert("", tk.END, values=data)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to display loans: {str(e)}")
