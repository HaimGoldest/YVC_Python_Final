import tkinter as tk
from tkinter import messagebox, ttk

import database_manager


class BookWaitingListWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.books_data = None
        self.members_data = None
        self.db_manager = database_manager.DatabaseManager()

        self.title("Waiting List By Book")

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

        # books_label
        books_label = tk.Label(self, text="Book Details", font=("Arial", 16))
        books_label.pack(pady=10)

        # Treeview widget for displaying books (limited to 1 row)
        self.books_table = ttk.Treeview(self, columns=("BookID", "Title", "Author", "Release Year", "Genre",
                                                       "Shelf Location", "Status"), show="headings")
        self.books_table.heading("BookID", text="Book ID")  # Adjust heading text for clarity
        self.books_table.heading("Title", text="Title")
        self.books_table.heading("Author", text="Author")
        self.books_table.heading("Release Year", text="Release Year")
        self.books_table.heading("Genre", text="Genre")
        self.books_table.heading("Shelf Location", text="Shelf Location")
        self.books_table.heading("Status", text="Status")

        # Set column widths
        self.books_table.column("#0", width=0)  # Hide the first empty column
        self.books_table.column("BookID", width=100)
        self.books_table.column("Title", width=150)
        self.books_table.column("Author", width=150)
        self.books_table.column("Release Year", width=100)
        self.books_table.column("Genre", width=150)
        self.books_table.column("Shelf Location", width=100)
        self.books_table.column("Status", width=150)

        self.books_table.configure(height=1)
        self.books_table.pack(padx=10, pady=10, fill=tk.X)

        # waiting_list_label
        waiting_list_label = tk.Label(self, text="Waiting Members", font=("Arial", 16))
        waiting_list_label.pack(pady=10)

        # Treeview widget for displaying members
        self.members_table = ttk.Treeview(self, columns=("MemberID", "Name", "Email", "Phone", "MembershipStartDate"),
                                          show="headings")
        self.members_table.heading("MemberID", text="Member ID")
        self.members_table.heading("Name", text="Name")
        self.members_table.heading("Email", text="Email")
        self.members_table.heading("Phone", text="Phone")
        self.members_table.heading("MembershipStartDate", text="Membership Start Date")
        self.members_table.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Close button
        self.close_button = tk.Button(self, text="Close", command=self.destroy)
        self.close_button.pack(padx=10, pady=10)

    def search_book(self):
        book_id = self.book_id_entry.get()

        try:
            # Attempt to get book data using get_book_by_id
            book_data = self.get_book_by_id(book_id)

            if book_data:  # Check if book data is not None
                self.fill_book_details(book_data)
                self.fill_members_details(book_data)
            else:
                messagebox.showinfo("Error", "Book not found!")
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
                    "BookID": book_data_list[0],
                    "Title": book_data_list[1],
                    "Author": book_data_list[2],
                    "ReleaseYear": book_data_list[3],
                    "Genre": book_data_list[4],
                    "ShelfLocation": book_data_list[5],
                    "Status": book_data_list[6]
                }

            return book_data_dict

        except Exception as e:  # Catch any exceptions during database operations
            print(f"Error retrieving book data: {str(e)}")
            return {}  # Return empty dictionary on error

    def fill_book_details(self, book_data):
        # Clear the books_table before adding new value
        self.books_table.delete(*self.books_table.get_children())

        # Extract the data
        book_id = book_data.get('BookID', '')
        title = book_data.get('Title', '')
        author = book_data.get('Author', '')
        release_year = book_data.get('ReleaseYear', '')
        genre = book_data.get('Genre', '')
        shelf_location = book_data.get('ShelfLocation', '')
        status = book_data.get('Status', '')

        # Insert the data to the TreeView
        self.books_table.insert('', 'end', values=(
            book_id, title, author, release_year, genre, shelf_location, status))

    def fill_members_details(self, book_data):
        # Clear the Treeview before filling with new data
        self.members_table.delete(*self.members_table.get_children())

        members_id_list = self.get_members_by_book(book_data)
        # if members_id_list is empty return without adding to members_table
        if not members_id_list:
            return

        conditions = []
        for member_id in members_id_list:
            conditions.append(f"MemberID = {member_id}")

        # Combine conditions
        if conditions:
            conditions = " OR ".join(conditions)
        else:
            conditions = None

        # Get members
        self.members_data = self.db_manager.read_from_table("members", "*", conditions)

        # Fill the Treeview with members data
        for member in self.members_data:
            self.members_table.insert("", tk.END, values=member)

    def get_members_by_book(self, book_data):
        book_id = book_data.get('BookID', '')
        columns = "*"
        conditions = f"BookID = {book_id}"
        waiting_list_data = self.db_manager.read_from_table("waiting_list", columns, conditions)
        members_id_list = [item[1] for item in waiting_list_data]

        return members_id_list
