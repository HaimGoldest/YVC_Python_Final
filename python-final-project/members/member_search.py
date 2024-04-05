import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import database_manager


class SearchMembersWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.members_data = None
        self.db_manager = database_manager.DatabaseManager()

        self.title("Search Members")

        # Title label (centered at the top)
        title_label = tk.Label(self, text="Search For Members", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)

        # Labels and entry fields for search criteria (arranged in a frame)
        search_frame = tk.Frame(self)
        search_frame.pack(pady=10)

        name_label = tk.Label(search_frame, text="Name:")
        name_label.pack(side=tk.LEFT)
        self.name_entry = tk.Entry(search_frame, width=30)
        self.name_entry.pack(side=tk.LEFT)

        email_label = tk.Label(search_frame, text="Email:")
        email_label.pack(side=tk.LEFT, padx=10)
        self.email_entry = tk.Entry(search_frame, width=30)
        self.email_entry.pack(side=tk.LEFT)

        phone_label = tk.Label(search_frame, text="Phone:")
        phone_label.pack(side=tk.LEFT, padx=10)
        self.phone_entry = tk.Entry(search_frame, width=30)
        self.phone_entry.pack(side=tk.LEFT)

        # Search and Clear buttons (centered horizontally)
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        self.search_button = tk.Button(button_frame, text="Search", command=self.search_members, width=10)
        self.search_button.pack(side=tk.LEFT, padx=(10, 0))  # Padding on left side only

        self.clear_button = tk.Button(button_frame, text="Clear", command=self.clear_fields, width=10)
        self.clear_button.pack(side=tk.LEFT, padx=(0, 10))  # Padding on right side only

        # Treeview for displaying members with field titles in the first row
        self.members_table = ttk.Treeview(self, columns=("MemberID", "Name", "Email", "Phone", "MembershipStartDate"),
                                          show="headings")
        self.members_table.heading("MemberID", text="Member ID")
        self.members_table.heading("Name", text="Name")
        self.members_table.heading("Email", text="Email")
        self.members_table.heading("Phone", text="Phone")
        self.members_table.heading("MembershipStartDate", text="Membership Start Date")
        self.members_table.pack(pady=10)

        # Close button (centered at the bottom)
        self.close_button = tk.Button(self, text="Close", command=self.destroy, width=10)
        self.close_button.pack(pady=10)

    def clear_fields(self):
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)

    def search_members(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()

        # Build conditions based on user input
        conditions = []
        if name:
            conditions.append(f"Name LIKE '%{name}%'")
        if email:
            conditions.append(f"Email LIKE '%{email}%'")
        if phone:
            conditions.append(f"Phone LIKE '%{phone}%'")

        # Combine conditions
        if conditions:
            conditions = " AND ".join(conditions)
        else:
            conditions = None

        # Retrieve members from database
        self.members_data = self.db_manager.read_from_table("members", "*", conditions)

        # Clear previous table data
        self.members_table.delete(*self.members_table.get_children())

        # Fill the Treeview with search results
        if self.members_data:
            for member in self.members_data:
                self.members_table.insert("", tk.END, values=member)
        else:
            messagebox.showinfo("No Results Found", "No members match your search criteria.")

