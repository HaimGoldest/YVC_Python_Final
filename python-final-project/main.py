import library_app_window
from login_window import LoginWindow
from static_models.user_model import UserDataModel

if __name__ == "__main__":
    # Open LoginWindow
    user_data = UserDataModel()
    login_window = LoginWindow(user_data)
    login_window.mainloop()

    if user_data.get_user_name():
        # Open LibraryApp only if login was successful
        app = library_app_window.LibraryApp()
        app.mainloop()
