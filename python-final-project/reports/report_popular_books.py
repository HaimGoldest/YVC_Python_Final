import tkinter as tk
from tkinter import ttk, messagebox

import database_manager


class PopularBooksReportWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.db_manager = database_manager.DatabaseManager()

        self.title("Popular Books Report")

        # Treeview widget for displaying popular books
        self.books_table = ttk.Treeview(self, columns=("BookID", "Book Title", "Loans Count"), show="headings")
        self.books_table.heading("BookID", text="Book ID")
        self.books_table.heading("Book Title", text="Book Title")
        self.books_table.heading("Loans Count", text="Loans Count")

        # Set column widths (adjust pixel values as needed)
        self.books_table.column("#0", width=0)  # Hide the first empty column
        self.books_table.column("BookID", width=100)
        self.books_table.column("Book Title", width=200)
        self.books_table.column("Loans Count", width=150)

        self.books_table.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Get popular books data
        self.books_data = self.get_popular_books()

        # Fill the Treeview with book data
        self.fill_treeview()

        # Close button
        self.close_button = tk.Button(self, text="Close", command=self.destroy)
        self.close_button.pack(padx=10, pady=10)

    def get_popular_books(self):
        query = """
            SELECT
                books.BookID,
                books.Title AS BookTitle,
                COUNT(loans.BookID) AS LoansCount
            FROM loans
            JOIN books ON loans.BookID = books.BookID
            GROUP BY books.BookID, books.Title
            ORDER BY LoansCount DESC;
        """
        return self.db_manager.execute_query(query)

    def fill_treeview(self):
        if not self.books_data:
            messagebox.showerror("Info", "No popular books found!")
            return

        try:
            for book in self.books_data:
                book_id, book_title, loans_count = book
                data = (book_id, book_title, loans_count)
                self.books_table.insert("", tk.END, values=data)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to display popular books: {str(e)}")
