import tkinter as tk
from tkinter import ttk

import database_manager


class ShowAllMembersWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.db_manager = database_manager.DatabaseManager()

        self.title("All Members")

        # Treeview widget for displaying members
        self.members_table = ttk.Treeview(self, columns=("MemberID", "Name", "Email", "Phone", "MembershipStartDate"),
                                          show="headings")
        self.members_table.heading("MemberID", text="Member ID")
        self.members_table.heading("Name", text="Name")
        self.members_table.heading("Email", text="Email")
        self.members_table.heading("Phone", text="Phone")
        self.members_table.heading("MembershipStartDate", text="Membership Start Date")
        self.members_table.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Get all members
        self.members_data = self.db_manager.read_from_table("members", "*")

        # Fill the Treeview with members data
        for member in self.members_data:
            self.members_table.insert("", tk.END, values=member)

        # Close button
        self.close_button = tk.Button(self, text="Close", command=self.destroy)
        self.close_button.pack(padx=10, pady=10)
