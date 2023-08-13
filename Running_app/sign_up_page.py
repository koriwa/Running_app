import tkinter as tk
import subprocess
import re
from PIL import ImageTk, Image
import customtkinter


# Initialize the customtkinter appearance and color theme
customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")

# Create the main GUI window
sign_up_page = tk.Tk()
sign_up_page.geometry("495x595")
sign_up_page.resizable(width=False, height=False)
sign_up_page.title('Sign Up')

# Define the accounts file path
ACCOUNTS_FILE = "db/accounts.txt"

# Centers the window
def center_window(window):
    """
    Centers the specified window on the screen.

    Args:
        window: The tkinter window to be centered.
    """
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    center_x = (screen_width - width) // 2
    center_y = (screen_height - height) // 2

    window.geometry(f"{width}x{height}+{center_x}+{center_y}")


# Center the sign-up page
center_window(sign_up_page)

# Function to display an error message
def show_error_message():
    """Display an error message for a short duration."""
    error_label.config(text="User already exists, please create a different account")
    sign_up_page.after(2000, lambda: error_label.config(text=""))

# Function to handle the sign-up process


def sign_up_button_function():
    """Handle the sign-up process."""
    # Get the entered values from the input fields
    username = User_name_box.get()
    password = Password_box.get()
    confirm_password = confirm_password_box.get()

    # Reset the error label text
    error_label.config(text="")

    # Check if the username or password fields are empty
    if not username or not password:
        error_label.config(text="Please enter a valid username and password")
        sign_up_page.after(3000, lambda: error_label.config(text=""))
        print("return 4")
        return

    # Check if the password matches the confirm password
    if password == confirm_password:
        # Check password length
        if len(password) < 8:
            error_label.config(text="Password must be at least 8 characters")
            sign_up_page.after(3000, lambda: error_label.config(text=""))
            print("return 3")
            return

        # Check for at least one capital letter and one digit using regular expressions
        if not (re.search(r"[A-Z]", password) and re.search(r"\d", password)):
            error_label.config(text="Password must contain one capital letter and one digit",
                               font=('Century Gothic', 7, "bold"))
            sign_up_page.after(3000, lambda: error_label.config(text=""))
            print("return 2")
            return

        # Open the accounts file in read and write mode
        with open(ACCOUNTS_FILE, "r+", encoding='utf-8') as file:
            # Read all the lines from the file
            lines = file.readlines()
            for line in lines:
                account_line = line.split(":")
                account_username = account_line[0].strip()

                # Check if the combination of username and password already exists in the file
                if username.strip() == account_username:
                    # Display an error message if the user already exists
                    error_label.config(text="Username already exists", font=(
                        'Century Gothic', 7, "bold"))
                    sign_up_page.after(
                        3000, lambda: error_label.config(text=""))
                    print("return 1")
                    return
            print("hi")
            # If the combination doesn't exist,
            # write the new username and password to the file and save it
            file.write(username + ":" + password + "\n")
            # Go back to the beginning of the file to update it
            file.seek(0)
            # Read all the lines again to update the lines variable
            lines = file.readlines()

        # Destroy the sign-up page
        sign_up_page.destroy()
        # Import the log-in page so the user can enter their credentials
        subprocess.Popen(["python", "log_in_page.py"])
    else:
        error_label.config(text="Invalid username or password")
        # Hide the error message after 3 seconds
        sign_up_page.after(3000, lambda: error_label.config(text=""))


def back_button_function():
    """Handle the back button action."""
    sign_up_page.destroy()
    subprocess.Popen(["python", "log_in_page.py"])


# Create the background image
BACKGROUND = "assets/sign_up_page_3.png"
background_image = ImageTk.PhotoImage(Image.open(BACKGROUND))

# Create a label with the background image
background_label = customtkinter.CTkLabel(
    master=sign_up_page, image=background_image)
background_label.pack()

# Create a frame for the sign-up form
frame = tk.Frame(master=background_label, width=320, height=400, bg="white")
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Create the error label
error_label = tk.Label(master=frame, text="", fg="red",
                       bg="white", font=('Century Gothic', 9, "bold"))
error_label.place(relx=0.48, y=240, anchor=tk.CENTER)

# Create the "Sign Up" label
login_label = customtkinter.CTkLabel(
    master=frame, text="Sign Up", font=('Century Gothic', 30))
login_label.place(x=110, y=45)

# Create the username input field
User_name_box = customtkinter.CTkEntry(
    master=frame, width=220, placeholder_text='Username', corner_radius=10)
User_name_box.place(x=50, y=110)

# Create the password input field
Password_box = customtkinter.CTkEntry(
    master=frame, width=220, placeholder_text='Password', corner_radius=10, show='*')
Password_box.place(x=50, y=155)

# Create the confirm password input field
confirm_password_box = customtkinter.CTkEntry(
    master=frame, width=220, placeholder_text='Confirm Password', corner_radius=10, show='*')
confirm_password_box.place(x=50, y=200)

# Create the "Sign Up" button
sign_up_button = customtkinter.CTkButton(master=frame, width=220, text="Sign Up",
                                         command=sign_up_button_function, corner_radius=100,
                                         fg_color="#FFBF00", hover_color="dark orange")
sign_up_button.place(x=50, y=255)

# Create the "back" button
back_button = customtkinter.CTkButton(master=frame, width=220, text="back",
                                      command=back_button_function,
                                      corner_radius=100, fg_color="#FFBF00",
                                      hover_color="dark orange")
back_button.place(x=50, y=305)

# Start the GUI event loop
sign_up_page.mainloop()
