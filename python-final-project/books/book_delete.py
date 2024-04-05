import tkinter as tk
from tkinter import messagebox

import database_manager


class DeleteBookWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.db_manager = database_manager.DatabaseManager()

        self.title("Delete Book")
        self.geometry("350x150")

        # Label for book ID entry
        self.book_id_label = tk.Label(self, text="Enter Book ID (will be permanently deleted):")
        self.book_id_label.pack(padx=10, pady=10)

        # Entry field for book ID
        self.book_id_entry = tk.Entry(self)
        self.book_id_entry.pack(padx=10, pady=5)

        # Button frame
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(padx=10, pady=10)

        # Delete button
        self.delete_button = tk.Button(self.button_frame, text="Delete", command=self.delete_book)
        self.delete_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Cancel button
        self.cancel_button = tk.Button(self.button_frame, text="Cancel", command=self.destroy)
        self.cancel_button.pack(side=tk.RIGHT, padx=10, pady=5)

    def delete_book(self):
        book_id = self.book_id_entry.get()

        if not book_id:  # Check if book ID is empty
            messagebox.showerror("Error", "Please enter a book ID to delete.")
            return  # Exit the function if no book ID

        try:
            self.db_manager.delete_from_table("books", f"BookID = {book_id}")
            messagebox.showinfo("Success", "Book deleted successfully!")
            self.destroy()  # Close the window
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while deleting the book: {str(e)}")
            self.destroy()  # Close the window


