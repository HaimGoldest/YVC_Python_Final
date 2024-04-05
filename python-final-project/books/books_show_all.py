import tkinter as tk
from tkinter import ttk

import database_manager


class ShowAllBooksWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.db_manager = database_manager.DatabaseManager()

        self.title("All Books")

        # Treeview widget for displaying books
        self.books_table = ttk.Treeview(self, columns=("BookID", "Title", "Author", "Release Year", "Genre",
                                                       "Shelf Location", "Status"), show="headings")
        self.books_table.heading("BookID", text="Book ID")  # Adjust heading text for clarity
        self.books_table.heading("Title", text="Title")
        self.books_table.heading("Author", text="Author")
        self.books_table.heading("Release Year", text="Release Year")
        self.books_table.heading("Genre", text="Genre")
        self.books_table.heading("Shelf Location", text="Shelf Location")
        self.books_table.heading("Status", text="Status")
        self.books_table.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Get all books
        self.books_data = self.db_manager.read_from_table("books", "*")

        # Fill the Treeview with book data
        for book in self.books_data:
            self.books_table.insert("", tk.END, values=book)

        # Close button
        self.close_button = tk.Button(self, text="Close", command=self.destroy)
        self.close_button.pack(padx=10, pady=10)
