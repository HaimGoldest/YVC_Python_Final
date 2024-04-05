import tkinter as tk
from tkinter import messagebox

import database_manager


class AddBookWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.db_manager = database_manager.DatabaseManager()

        self.title("Add Book")
        self.geometry("300x200")

        # Labels for input fields
        title_label = tk.Label(self, text="Title:")
        title_label.grid(row=0, column=0, padx=10, pady=5)
        author_label = tk.Label(self, text="Author:")
        author_label.grid(row=1, column=0, padx=10, pady=5)
        release_year_label = tk.Label(self, text="Release Year:")
        release_year_label.grid(row=2, column=0, padx=10, pady=5)
        genre_label = tk.Label(self, text="Genre:")
        genre_label.grid(row=3, column=0, padx=10, pady=5)
        shelf_location_label = tk.Label(self, text="Shelf Location:")
        shelf_location_label.grid(row=4, column=0, padx=10, pady=5)

        # Entry fields
        self.title_entry = tk.Entry(self)
        self.title_entry.grid(row=0, column=1, padx=10, pady=5)
        self.author_entry = tk.Entry(self)
        self.author_entry.grid(row=1, column=1, padx=10, pady=5)
        self.release_year_entry = tk.Entry(self)
        self.release_year_entry.grid(row=2, column=1, padx=10, pady=5)
        self.genre_entry = tk.Entry(self)
        self.genre_entry.grid(row=3, column=1, padx=10, pady=5)
        self.shelf_location_entry = tk.Entry(self)
        self.shelf_location_entry.grid(row=4, column=1, padx=10, pady=5)

        # Buttons
        self.add_book_button = tk.Button(self, text="Add Book", command=self.add_book, state=tk.DISABLED)
        self.add_book_button.grid(row=5, column=0, columnspan=1, padx=10, pady=10)
        self.cancel_button = tk.Button(self, text="Cancel", command=self.destroy)
        self.cancel_button.grid(row=5, column=1, columnspan=1, padx=10, pady=10)
        # Bind validation to entry fields
        self.title_entry.bind("<KeyRelease>", self.validate_fields)
        self.author_entry.bind("<KeyRelease>", self.validate_fields)
        self.release_year_entry.bind("<KeyRelease>", self.validate_fields)
        self.genre_entry.bind("<KeyRelease>", self.validate_fields)
        self.shelf_location_entry.bind("<KeyRelease>", self.validate_fields)

    def validate_fields(self, event):
        # Check if all entry fields are filled
        all_fields_filled = (
                self.title_entry.get() and
                self.author_entry.get() and
                self.release_year_entry.get() and
                self.genre_entry.get() and
                self.shelf_location_entry.get()
        )

        # Enable or disable the "Add Book" button based on validation
        self.add_book_button.config(state=tk.NORMAL if all_fields_filled else tk.DISABLED)

    def add_book(self):
        try:
            # Get book details from entry fields
            title = self.title_entry.get()
            author = self.author_entry.get()
            release_year = int(self.release_year_entry.get())
            genre = self.genre_entry.get()
            shelf_location = self.shelf_location_entry.get()

            # Create a dictionary with book details
            book_data = {
                "Title": title,
                "Author": author,
                "ReleaseYear": release_year,
                "Genre": genre,
                "ShelfLocation": shelf_location,
                "Status": "Available"  # Set status as "Available" by default
            }

            # Use the DatabaseManager to add the book
            self.db_manager.add_to_table("books", book_data)  # Pass dictionary instead of string

            messagebox.showinfo("Success", "Book added successfully!")
            # Clear entry fields after successful addition
            self.title_entry.delete(0, tk.END)
            self.author_entry.delete(0, tk.END)
            self.release_year_entry.delete(0, tk.END)
            self.genre_entry.delete(0, tk.END)
            self.shelf_location_entry.delete(0, tk.END)
        except Exception as e:  # Catch any database-related errors
            messagebox.showerror("Error", "Failed to add book: {}".format(str(e)))
