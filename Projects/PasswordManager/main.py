from tkinter import *
from tkinter import messagebox
import re
import random
import string
import pyperclip


# --------------------------- PASSWORD GENERATOR ---------------------------- #
def generate_password(length=12):
    if length < 8:  # Ensure a reasonable password length
        length = 8

    # Define the possible characters for the password
    characters = string.ascii_letters + string.digits + string.punctuation

    # Generate a random password
    password = ''.join(random.choice(characters) for i in range(length))
    password_entry.delete(0, END)
    password_entry.insert(END, string=password)
    pyperclip.copy(password)  # Copy password to clipboard


# ---------------------------- SAVE PASSWORD -------------------------------- #
def validate_email(email):
    pattern = (
        r'(?:[a-zA-Z0-9_'
        '^&/+-]+(?:\.[a-zA-Z0-9_'
        '^&/+-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\'
        + r'[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}|'
        + r'(?:\d{1,3}\.){3}\d{1,3}(?::\d{1,5})?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.)'
        + r'{3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-zA-Z\-]*[a-zA-Z]:'
        + r'(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)])'
    )
    return re.match(pattern, email)


def validate_password(password):
    # Check if password is at least 8 characters
    return len(password) >= 8


def validate_website(website):
    # Check if website isn't empty
    return len(website) > 0


def save_password():
    website = website_entry.get()
    email = email_username_entry.get()
    password = password_entry.get()

    if not validate_email(email):
        messagebox.showerror("Invalid email", f"Email '{email}' is not valid.")
    elif not validate_password(password):
        messagebox.showerror(
            "Invalid password", f"Password is too short. Minimum 8 characters long."
        )
    elif not validate_website(website):
        messagebox.showerror("Website cannot be empty", f"Please type a website name")
    else:  # All fields are valid
        is_ok = messagebox.askokcancel(
            title=website,
            message=f"These are the details entered: \nEmail: {email}"
            f"\nPassword: {password}\nIs it OK to save?",
        )

        if is_ok:
            with open("data.txt", mode="a+") as file:
                file.write(f"{website} | {email} | {password}\n")
                website_entry.delete(0, END)
                password_entry.delete(0, END)


# ------------------------------- UI SETUP ---------------------------------- #
# Window Setup
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Get image
logo_img = PhotoImage(file='logo.png')

# Canvas setup
canvas = Canvas(width=200, height=200)
# Background Image
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Form fields
# Website Field
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)
website_entry = Entry()
website_entry.grid(column=1, row=1, columnspan=2, sticky="EW")
website_entry.focus()

# Email/Username Field
email_username_label = Label(text="Email/Username:")
email_username_label.grid(column=0, row=2)
email_username_entry = Entry()
email_username_entry.insert(END, string="brian.arriaga@gmail.com")
email_username_entry.grid(column=1, row=2, columnspan=2, sticky="EW")

# Password Field
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)
password_entry = Entry()
password_entry.grid(column=1, row=3, sticky="EW")

# Buttons
password_gen_btn = Button(text="Generate Password", command=generate_password)
password_gen_btn.grid(column=2, row=3, sticky="EW")
add_btn = Button(text="Add", width=35, command=save_password)
add_btn.grid(column=1, row=4, columnspan=2, sticky="EW")


window.mainloop()
