import tkinter as tk

from members import member_add, member_edit, member_delete, member_search, members_show_all


class MembersManagementWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)  # Inherit from Toplevel for a new window
        self.title("Members Management")
        self.geometry("400x300")

        # Create header frame
        header_frame = tk.Frame(self, bg="lightblue", height=50)
        header_frame.pack(fill=tk.X)

        # Create header label
        header_label = tk.Label(header_frame, text="Members Management", font=("Arial", 18, "bold"))
        header_label.pack()

        # Create button frame
        button_frame = tk.Frame(self)
        button_frame.pack(padx=10, pady=10)

        # Create buttons with vertical layout
        button_list = ["Show All Members", "Find Members", "Add Members", "Edit Members", "Delete Members", "Close"]
        for button_text in button_list:
            button = tk.Button(button_frame, text=button_text, command=lambda b=button_text: self.button_clicked(b))
            button.pack(fill=tk.X, pady=5)

    def button_clicked(self, button_text):
        if button_text.startswith("Add"):
            member_add.AddMemberWindow(self)  # Create AddMemberWindow
        elif button_text.startswith("Edit"):
            member_edit.EditMemberWindow(self)  # Create EditMemberWindow
        elif button_text.startswith("Delete"):
            member_delete.DeleteMemberWindow(self)  # Create DeleteMemberWindow
        elif button_text.startswith("Find"):
            member_search.SearchMembersWindow(self)  # Create SearchMembersWindow
        elif button_text.startswith("Show"):
            members_show_all.ShowAllMembersWindow(self)  # Create ShowAllMembersWindow
        elif button_text.startswith("Close"):
            self.destroy()  # Close the window
