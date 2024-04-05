import tkinter as tk
from tkinter import ttk, messagebox

from datetime import datetime

import database_manager


class LoanReturnedWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.is_saving_enabled = False
        self.db_manager = database_manager.DatabaseManager()
        self.loan_data_dict = {}

        self.title("Loan Return")

        # Frame for loan ID search
        self.search_frame = tk.Frame(self)
        self.search_frame.pack(padx=10, pady=10)

        # Label and entry for loan ID search
        loan_id_label = tk.Label(self.search_frame, text="Enter Loan ID:")
        loan_id_label.pack(side=tk.LEFT)
        self.loan_id_entry = tk.Entry(self.search_frame)
        self.loan_id_entry.pack(side=tk.LEFT, padx=10)

        # Button to search for loan details
        search_button = tk.Button(self.search_frame, text="Search", command=self.search_loan)
        search_button.pack(side=tk.RIGHT)

        # Treeview widget for displaying loan details (limited to 1 row)
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

        # Set column widths
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

        self.loans_table.configure(height=1)
        self.loans_table.pack(padx=10, pady=10, fill=tk.X)

        # Create buttons for saving and canceling
        self.save_button = tk.Button(self, text="Save book return", command=self.update_book_returned,
                                     state=tk.DISABLED)
        self.save_button.pack(padx=10, pady=10)
        self.cancel_button = tk.Button(self, text="Cancel", command=self.destroy)
        self.cancel_button.pack(padx=10, pady=10)

    def search_loan(self):
        loan_id = self.loan_id_entry.get()
        try:
            # Attempt to get loan data using get_loan_by_id
            loan_data_list = self.get_loan_by_id(loan_id)[0]

            if loan_data_list:
                self.loan_data_dict = {
                    "LoanID": loan_data_list[0],
                    "MemberID": loan_data_list[1],
                    "MemberName": loan_data_list[2],
                    "BookID": loan_data_list[3],
                    "BookTitle": loan_data_list[4],
                    "BookStatus": loan_data_list[5],
                    "LoanDate": loan_data_list[6],
                    "DueDate": loan_data_list[7],
                    "ReturnDate": loan_data_list[8]
                }

                self.fill_details()
                self.is_saving_enabled = True  # Enable save button
            else:
                messagebox.showinfo("Error", "Loan not found!")

            self.update_save_button_state()  # Update button state based on flag
        except Exception as e:  # Catch any exceptions during database operations
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def get_loan_by_id(self, loan_id):
        query = 'SELECT loans.LoanID, loans.MemberID, members.Name AS MemberName, loans.BookID, ' \
                'books.Title AS BookTitle, books.Status AS BookStatus, loans.LoanDate, loans.DueDate, ' \
                'loans.ReturnDate\n' \
                'FROM loans\n' \
                'JOIN books ON loans.BookID = books.BookID\n' \
                'JOIN members ON loans.MemberID = members.MemberID\n' \
                f'WHERE loans.LoanID = {loan_id};'
        return self.db_manager.execute_query(query)

    def fill_details(self):
        # Extract the data to be displayed from the loan_data_dict
        loan_id = self.loan_data_dict.get('LoanID', '')
        member_id = self.loan_data_dict.get('MemberID', '')
        member_name = self.loan_data_dict.get('MemberName', '')
        book_id = self.loan_data_dict.get('BookID', '')
        book_title = self.loan_data_dict.get('BookTitle', '')
        book_status = self.loan_data_dict.get('BookStatus', '')
        loan_date = self.loan_data_dict.get('LoanDate', '')
        due_date = self.loan_data_dict.get('DueDate', '')
        return_date = self.loan_data_dict.get('ReturnDate', '')

        # Insert the data to the TreeView
        self.loans_table.insert('', 'end', values=(
            loan_id, member_id, member_name, book_id, book_title, book_status, loan_date, due_date, return_date))

    def update_save_button_state(self):
        self.save_button.config(state=tk.NORMAL if self.is_saving_enabled else tk.DISABLED)

    def update_book_returned(self):
        loan_id = self.loan_data_dict.get('LoanID', '')
        book_id = self.loan_data_dict.get('BookID', '')
        book_status = self.loan_data_dict.get('BookStatus', '')

        if book_status == "Available":
            messagebox.showwarning("Warning", "This book is already available!")
            return

        try:
            self.update_book_status(book_id)
            self.update_return_date(loan_id)
            messagebox.showinfo("Success", "Loan was returned successfully!")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", "Failed to return loan: {}".format(str(e)))

    def update_book_status(self, book_id):
        values = {
            "Status": 'Available',
        }
        condition = f"BookID LIKE {book_id}"
        self.db_manager.update_table("books", values, condition)

    def update_return_date(self, loan_id):
        values = {
            "ReturnDate": datetime.today().strftime('%Y-%m-%d')
        }
        condition = f"LoanID LIKE {loan_id}"
        self.db_manager.update_table("loans", values, condition)
