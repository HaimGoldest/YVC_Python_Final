import tkinter as tk
from tkinter import messagebox

import database_manager


class DeleteMemberWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.db_manager = database_manager.DatabaseManager()

        self.title("Delete Member")
        self.geometry("350x150")

        # Label for member ID entry
        self.member_id_label = tk.Label(self, text="Enter Member ID (will be permanently deleted):")
        self.member_id_label.pack(padx=10, pady=10)

        # Entry field for member ID
        self.member_id_entry = tk.Entry(self)
        self.member_id_entry.pack(padx=10, pady=5)

        # Button frame
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(padx=10, pady=10)

        # Delete button
        self.delete_button = tk.Button(self.button_frame, text="Delete", command=self.delete_member)
        self.delete_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Cancel button
        self.cancel_button = tk.Button(self.button_frame, text="Cancel", command=self.destroy)
        self.cancel_button.pack(side=tk.RIGHT, padx=10, pady=5)

    def delete_member(self):
        member_id = self.member_id_entry.get()

        if not member_id:  # Check if member ID is empty
            messagebox.showerror("Error", "Please enter a member ID to delete.")
            return  # Exit the function if no member ID

        try:
            self.db_manager.delete_from_table("members", f"MemberID = {member_id}")
            messagebox.showinfo("Success", "Member deleted successfully!")
            self.destroy()  # Close the window
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while deleting the member: {str(e)}")
            self.destroy()  # Close the window


