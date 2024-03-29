import tkinter as tk
from tkinter import messagebox


def ask_quit():
    """Creates a windows asking the user if they want to quit the app or stay

    Returns:
        Bool: True or False (Yes or No)
    """
    # Create a new window
    window = tk.Tk()
    window.withdraw()  # Hide the main window

    # Ask user with a messagebox
    response = messagebox.askyesno("Quit", "Do you want to quit?")

    if response:
        print("Quitting...")
        return response
    else:
        print("Continuing...")
        return response

    window.destroy()
