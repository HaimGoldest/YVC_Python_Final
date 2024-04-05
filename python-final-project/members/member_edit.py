import tkinter as tk
from tkinter import messagebox

import re

import database_manager


class EditMemberWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.is_saving_enabled = False
        self.db_manager = database_manager.DatabaseManager()

        self.title("Edit Member")

        # Frame for member ID search
        self.search_frame = tk.Frame(self)
        self.search_frame.pack(padx=10, pady=10)

        # Label and entry for member ID search
        member_id_label = tk.Label(self.search_frame, text="Enter Member ID:")
        member_id_label.pack(side=tk.LEFT)
        self.member_id_entry = tk.Entry(self.search_frame)
        self.member_id_entry.pack(side=tk.LEFT, padx=10)

        # Button to search for member details
        search_button = tk.Button(self.search_frame, text="Search", command=self.search_member)
        search_button.pack(side=tk.RIGHT)

        # Frame for member details (initially hidden)
        self.details_frame = tk.Frame(self)
        self.details_frame.pack_propagate(False)  # Prevent details frame from resizing
        self.details_frame.pack(padx=10, pady=10)

        # Labels and entry fields for member details
        name_label = tk.Label(self.details_frame, text="Name:")
        name_label.grid(row=0, column=0, padx=10, pady=5)
        self.name_entry = tk.Entry(self.details_frame)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        email_label = tk.Label(self.details_frame, text="Email:")
        email_label.grid(row=1, column=0, padx=10, pady=5)
        self.email_entry = tk.Entry(self.details_frame)
        self.email_entry.grid(row=1, column=1, padx=10, pady=5)

        phone_label = tk.Label(self.details_frame, text="Phone:")
        phone_label.grid(row=2, column=0, padx=10, pady=5)
        self.phone_entry = tk.Entry(self.details_frame)
        self.phone_entry.grid(row=2, column=1, padx=10, pady=5)

        # Create buttons for saving and canceling
        self.save_button = tk.Button(self, text="Save Changes", command=self.update_member,
                                     state=tk.DISABLED)
        self.save_button.pack(padx=10, pady=10)
        self.cancel_button = tk.Button(self, text="Cancel", command=self.destroy)
        self.cancel_button.pack(padx=10, pady=10)

    def update_member(self):
        member_id = self.member_id_entry.get()
        name = self.name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()

        # Validate email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):  # Basic email format check
            messagebox.showerror("Invalid email", "Please enter a valid email address.")
            return  # Exit the function if email is invalid

        try:
            # Continue with database update if email is valid
            values = {
                "Name": name,
                "Email": email,
                "Phone": phone
            }
            conditions = f"MemberID = {member_id}"
            self.db_manager.update_table("members", values, conditions)
            messagebox.showinfo("Success", "Member updated successfully!")
            self.destroy()  # Close the window
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while updating the member: {str(e)}")

    def search_member(self):
        member_id = self.member_id_entry.get()

        try:
            # Attempt to get member data using get_member_by_id
            member_data = self.get_member_by_id(member_id)

            if member_data:  # Check if member data is not None
                self.fill_details(member_data)
                self.details_frame.pack()  # Show details frame
                self.is_saving_enabled = True  # Enable save button
            else:
                messagebox.showinfo("Error", "Member not found!")

            self.update_save_button_state()  # Update button state based on flag

        except Exception as e:  # Catch any exceptions during database operations
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def get_member_by_id(self, member_id):
        columns = "*"
        conditions = f"MemberID = {member_id}"
        member_data_dict = {}

        try:
            # Attempt to read from the database
            member_data_list = self.db_manager.read_from_table("members", columns, conditions)[0]
            if member_data_list:
                member_data_dict = {
                    "Name": member_data_list[1],
                    "Email": member_data_list[2],
                    "Phone": member_data_list[3],
                    "MembershipStartDate": member_data_list[4]
                }

            return member_data_dict

        except Exception as e:  # Catch any exceptions during database operations
            print(f"Error retrieving member data: {str(e)}")
            return {}  # Return empty dictionary on error

    def fill_details(self, member_data):
        # Clear existing text in entry fields
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)

        # Fill entry fields with corresponding member data
        self.name_entry.insert(0, member_data.get("Name", ""))
        self.email_entry.insert(0, member_data.get("Email", ""))
        self.phone_entry.insert(0, member_data.get("Phone", ""))

    def update_save_button_state(self):
        self.save_button.config(state=tk.NORMAL if self.is_saving_enabled else tk.DISABLED)
