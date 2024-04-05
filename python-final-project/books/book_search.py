import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import database_manager


class SearchBooksWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.books_data = None
        self.db_manager = database_manager.DatabaseManager()

        self.title("Search Books")

        # Title label (centered at the top)
        title_label = tk.Label(self, text="Search For Books", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)

        # Labels and entry fields for search criteria (arranged in a frame)
        search_frame = tk.Frame(self)
        search_frame.pack(pady=10)

        title_label = tk.Label(search_frame, text="Title:")
        title_label.pack(side=tk.LEFT)
        self.title_entry = tk.Entry(search_frame, width=30)
        self.title_entry.pack(side=tk.LEFT)

        author_label = tk.Label(search_frame, text="Author:")
        author_label.pack(side=tk.LEFT, padx=10)  # Space between labels
        self.author_entry = tk.Entry(search_frame, width=30)
        self.author_entry.pack(side=tk.LEFT)

        category_label = tk.Label(search_frame, text="Category:")
        category_label.pack(side=tk.LEFT, padx=10)
        self.category_entry = tk.Entry(search_frame, width=30)
        self.category_entry.pack(side=tk.LEFT)

        release_year_label = tk.Label(search_frame, text="Release Year:")
        release_year_label.pack(side=tk.LEFT, padx=10)
        self.release_year_entry = tk.Entry(search_frame, width=10)
        self.release_year_entry.pack(side=tk.LEFT)

        # Search and Clear buttons (centered horizontally)
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        self.search_button = tk.Button(button_frame, text="Search", command=self.search_books, width=10)
        self.search_button.pack(side=tk.LEFT, padx=(10, 0))  # Padding on left side only

        self.clear_button = tk.Button(button_frame, text="Clear", command=self.clear_fields, width=10)
        self.clear_button.pack(side=tk.LEFT, padx=(0, 10))  # Padding on right side only

        # Treeview for displaying books with field titles in the first row
        self.books_table = ttk.Treeview(self, columns=(
            "BookID", "Title", "Author", "Release Year", "Genre", "Shelf Location", "Status"), show="headings")
        self.books_table.heading("BookID", text="Book ID")  # Adjust heading text for clarity
        self.books_table.heading("Title", text="Title")
        self.books_table.heading("Author", text="Author")
        self.books_table.heading("Release Year", text="Release Year")
        self.books_table.heading("Genre", text="Genre")
        self.books_table.heading("Shelf Location", text="Shelf Location")
        self.books_table.heading("Status", text="Status")
        self.books_table.pack(pady=10)

        # Close button (centered at the bottom)
        self.close_button = tk.Button(self, text="Close", command=self.destroy, width=10)
        self.close_button.pack(pady=10)

    def clear_fields(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.release_year_entry.delete(0, tk.END)

    def search_books(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        category = self.category_entry.get().strip()
        release_year = self.release_year_entry.get().strip()  # Get release year

        # Build conditions based on user input
        conditions = []
        if title:
            conditions.append(f"Title LIKE '%{title}%'")
        if author:
            conditions.append(f"Author LIKE '%{author}%'")
        if category:
            conditions.append(f"Genre LIKE '%{category}%'")
        if release_year:  # Check if release year is entered
            try:
                int(release_year)  # Validate input as integer
                conditions.append(f"ReleaseYear = {release_year}")
            except ValueError:
                messagebox.showerror("Invalid Release Year", "Please enter a valid year as an integer.")
                return  # Exit search if release year is invalid

        # Combine conditions
        if conditions:
            conditions = " AND ".join(conditions)
        else:
            conditions = None

        # Retrieve books from database
        self.books_data = self.db_manager.read_from_table("books", "*", conditions)

        # Clear previous table data
        self.books_table.delete(*self.books_table.get_children())

        # Fill the Treeview with search results
        if self.books_data:
            for book in self.books_data:
                self.books_table.insert("", tk.END, values=book)
        else:
            messagebox.showinfo("No Results Found", "No books match your search criteria.")

