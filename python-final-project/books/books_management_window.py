import tkinter as tk

from books import book_add, book_edit, book_delete, book_search, books_show_all


class BooksManagementWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)  # Inherit from Toplevel for a new window
        self.title("Books Management")
        self.geometry("400x300")

        # Create header frame
        header_frame = tk.Frame(self, bg="lightblue", height=50)
        header_frame.pack(fill=tk.X)  # Fill horizontally

        # Create header label
        header_label = tk.Label(header_frame, text="Books Management", font=("Arial", 18, "bold"))
        header_label.pack()

        # Create button frame
        button_frame = tk.Frame(self)
        button_frame.pack(padx=10, pady=10)

        # Create buttons with vertical layout
        button_list = ["Show All Books", "Find Book", "Add Book", "Edit Book", "Delete Book", "Close"]
        for button_text in button_list:
            button = tk.Button(button_frame, text=button_text, command=lambda b=button_text: self.button_clicked(b))
            button.pack(fill=tk.X, pady=5)  # Fill horizontally, add padding between buttons

    def button_clicked(self, button_text):
        if button_text.startswith("Add"):
            book_add.AddBookWindow(self)  # Create AddBookWindow
        elif button_text.startswith("Edit"):
            book_edit.EditBookWindow(self)  # Create EditBookWindow
        elif button_text.startswith("Delete"):
            book_delete.DeleteBookWindow(self)  # Create DeleteBookWindow
        elif button_text.startswith("Find"):
            book_search.SearchBooksWindow(self)  # Create SearchBooksWindow
        elif button_text.startswith("Show"):
            books_show_all.ShowAllBooksWindow(self)  # Create ShowAllBooksWindow
        elif button_text.startswith("Close"):
            self.destroy()  # Close the window
