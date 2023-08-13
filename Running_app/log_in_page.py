import tkinter as tk
import subprocess
import customtkinter
from PIL import ImageTk, Image

# Set the appearance mode for the customtkinter module
customtkinter.set_appearance_mode("light")

# Define the file containing account information
ACCOUNTS_FILE = r"db/accounts.txt"

# Function to handle the login button
def button_function_login():
    """
    Handles the login process:
    1. Retrieves the entered username and password.
    2. Checks if the entered credentials match any stored accounts.
    3. If successful, opens the timer application with the logged-in username.
    4. Displays appropriate error messages for invalid credentials or empty fields.
    """
    # Grab the username and password when they are inputted
    username = User_name_box.get()
    password = Password_box.get()

    # Check if the username and password match with the files
    login_successful = False  # Flag to track successful login

    # Open the accounts file for reading and writing
    with open(ACCOUNTS_FILE, 'r+', encoding='utf-8') as file:
        # Iterate through every line in the file
        for line in file:
            # Split the line into stored_username and stored_password
            stored_username, stored_password = line.strip().split(':')
            # Validate if the username and password match with the database
            if username == stored_username and password == stored_password:
                login_successful = True
                break  # Stop the loop as a match is found

    # If login is successful, close the window/page and open timer.py with the
    # username
    if login_successful:
        log_in_page.destroy()
        subprocess.Popen(["python", "timer.py", username.strip()])
    else:
        # Handle error cases: empty username, empty password, or invalid
        # credentials
        if username == "":
            error_label.config(text="please enter a username")
        elif password == "":
            error_label.config(text="please enter a password")
        else:
            error_label.config(text="Invalid username or password")

        # Hide the error message after 3 seconds
        log_in_page.after(3000, lambda: error_label.config(text=""))

# Function to handle the sign up button
def button_function_signup():
    """
    Handles the sign-up process:
    Closes the current login window and opens the sign-up page.
    """
    # Close the current window/page and open sign_up_page.py
    log_in_page.destroy()
    subprocess.Popen(["python", "sign_up_page.py"])


# Create the main sign-in page
log_in_page = tk.Tk()
log_in_page.geometry("495x595")
log_in_page.resizable(width=False, height=False)
log_in_page.title('Login')

# Function to center the window on the screen


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


# Center the main sign-in window
center_window(log_in_page)

# Load and display the background image
BACKGROUND_IMAGE_PATH = r"assets/background.png"
background_image = ImageTk.PhotoImage(Image.open(BACKGROUND_IMAGE_PATH))
background_label = tk.Label(master=log_in_page, image=background_image)
background_label.pack()

# Create a frame for the login components
frame = tk.Frame(master=background_label, width=320, height=400, bg="white")
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Create labels, input fields, and buttons for the login page
login_label = tk.Label(master=frame, text="Log into your Account",
                       font=('Century Gothic', 20), bg="white")
login_label.place(x=20, y=45)

# Create custom entry fields with placeholders
User_name_box = customtkinter.CTkEntry(
    master=frame,
    width=245,
    height=20,
    corner_radius=10,
    placeholder_text='Username',
    justify="center")
User_name_box.place(x=30, y=110)

Password_box = customtkinter.CTkEntry(
    master=frame,
    width=245,
    height=20,
    corner_radius=10,
    placeholder_text='Password',
    justify="center",
    show="*")
Password_box.place(x=30, y=165)

# Create custom buttons for login and sign up
login_button = customtkinter.CTkButton(master=frame, width=220, text="Login",
                                       command=button_function_login,
                                       corner_radius=100, fg_color="orange",
                                       hover_color="dark orange")
login_button.place(x=45, y=220)

sign_in_button = customtkinter.CTkButton(
    master=frame,
    width=220,
    text="Sign Up",
    command=button_function_signup,
    corner_radius=100,
    fg_color="#FFBF00",
    hover_color="dark orange")
sign_in_button.place(x=45, y=270)

# Create a label to display error messages
error_label = tk.Label(master=frame, text="", fg="red",
                       bg="white", font=('Century Gothic', 10, "bold"))
error_label.place(relx=0.48, y=205, anchor=tk.CENTER)

# Bind the login and sign up buttons to their respective functions
login_button.bind("<Button-1>", button_function_login)
sign_in_button.bind("<Button-1>", button_function_signup)

# Start the main event loop
log_in_page.mainloop()
