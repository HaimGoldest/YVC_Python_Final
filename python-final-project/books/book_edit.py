import tkinter as tk
from tkinter import messagebox

import database_manager


class EditBookWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.is_saving_enabled = False
        self.db_manager = database_manager.DatabaseManager()

        self.title("Edit Book")

        # Frame for book ID search
        self.search_frame = tk.Frame(self)
        self.search_frame.pack(padx=10, pady=10)

        # Label and entry for book ID search
        book_id_label = tk.Label(self.search_frame, text="Enter Book ID:")
        book_id_label.pack(side=tk.LEFT)
        self.book_id_entry = tk.Entry(self.search_frame)
        self.book_id_entry.pack(side=tk.LEFT, padx=10)

        # Button to search for book details
        search_button = tk.Button(self.search_frame, text="Search", command=self.search_book)
        search_button.pack(side=tk.RIGHT)

        # Frame for book details (initially hidden)
        self.details_frame = tk.Frame(self)
        self.details_frame.pack_propagate(False)  # Prevent details frame from resizing
        self.details_frame.pack(padx=10, pady=10)

        # Labels and entry fields for book details (modify as needed)
        title_label = tk.Label(self.details_frame, text="Title:")
        title_label.grid(row=0, column=0, padx=10, pady=5)
        self.title_entry = tk.Entry(self.details_frame)
        self.title_entry.grid(row=0, column=1, padx=10, pady=5)

        author_label = tk.Label(self.details_frame, text="Author:")
        author_label.grid(row=1, column=0, padx=10, pady=5)
        self.author_entry = tk.Entry(self.details_frame)
        self.author_entry.grid(row=1, column=1, padx=10, pady=5)

        release_year_label = tk.Label(self.details_frame, text="Release Year:")
        release_year_label.grid(row=2, column=0, padx=10, pady=5)
        self.release_year_entry = tk.Entry(self.details_frame)
        self.release_year_entry.grid(row=2, column=1, padx=10, pady=5)

        genre_label = tk.Label(self.details_frame, text="Genre:")
        genre_label.grid(row=3, column=0, padx=10, pady=5)
        self.genre_entry = tk.Entry(self.details_frame)
        self.genre_entry.grid(row=3, column=1, padx=10, pady=5)

        shelf_location_label = tk.Label(self.details_frame, text="Shelf Location:")
        shelf_location_label.grid(row=4, column=0, padx=10, pady=5)
        self.shelf_location_entry = tk.Entry(self.details_frame)
        self.shelf_location_entry.grid(row=4, column=1, padx=10, pady=5)

        # Create buttons for saving and canceling
        self.save_button = tk.Button(self, text="Save Changes", command=self.update_book,
                                     state=tk.DISABLED)
        self.save_button.pack(padx=10, pady=10)
        self.cancel_button = tk.Button(self, text="Cancel", command=self.destroy)
        self.cancel_button.pack(padx=10, pady=10)

    def update_book(self):
        book_id = self.book_id_entry.get()
        title = self.title_entry.get()
        author = self.author_entry.get()
        release_year = self.release_year_entry.get()
        genre = self.genre_entry.get()
        shelf_location = self.shelf_location_entry.get()

        try:
            values = {
                "Title": title,
                "Author": author,
                "ReleaseYear": release_year,
                "Genre": genre,
                "ShelfLocation": shelf_location,
            }
            conditions = f"BookID = {book_id}"
            self.db_manager.update_table("books", values, conditions)
            messagebox.showinfo("Success", "Book updated successfully!")
            self.destroy()  # Close the window
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while updating the book: {str(e)}")

    def search_book(self):
        book_id = self.book_id_entry.get()

        try:
            # Attempt to get book data using get_book_by_id
            book_data = self.get_book_by_id(book_id)

            if book_data:  # Check if book data is not None
                self.fill_details(book_data)
                self.details_frame.pack()  # Show details frame
                self.is_saving_enabled = True  # Enable save button
            else:
                messagebox.showinfo("Error", "Book not found!")

            self.update_save_button_state()  # Update button state based on flag
        except Exception as e:  # Catch any exceptions during database operations
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def get_book_by_id(self, book_id):
        columns = "*"
        conditions = f"BookID = {book_id}"
        book_data_dict = {}

        try:
            # Attempt to read from the database table
            book_data_list = self.db_manager.read_from_table("books", columns, conditions)[0]
            if book_data_list:
                book_data_dict = {
                    "Title": book_data_list[1],
                    "Author":  book_data_list[2],
                    "ReleaseYear":  book_data_list[3],
                    "Genre":  book_data_list[4],
                    "ShelfLocation":  book_data_list[5],
                    "Status": book_data_list[6]
                }

            return book_data_dict

        except Exception as e:  # Catch any exceptions during database operations
            print(f"Error retrieving book data: {str(e)}")
            return {}  # Return empty dictionary on error

    def fill_details(self, book_data):
        # Clear existing text in entry fields
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.release_year_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.shelf_location_entry.delete(0, tk.END)

        # Fill entry fields with corresponding book data
        self.title_entry.insert(0, book_data.get("Title", ""))
        self.author_entry.insert(0, book_data.get("Author", ""))
        self.release_year_entry.insert(0, book_data.get("ReleaseYear", ""))
        self.genre_entry.insert(0, book_data.get("Genre", ""))
        self.shelf_location_entry.insert(0, book_data.get("ShelfLocation", ""))

    def update_save_button_state(self):
        self.save_button.config(state=tk.NORMAL if self.is_saving_enabled else tk.DISABLED)
