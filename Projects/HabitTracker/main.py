from tkinter import Tk, Label, Entry, Button, messagebox, PhotoImage
from tkcalendar import Calendar
from datetime import datetime
import requests
import webbrowser
from dotenv import load_dotenv
from pathlib import Path
import os
import time

# Load environment variables from the .env file
ENV_PATH = Path("..", "..", ".env")
load_dotenv(dotenv_path=ENV_PATH)

# Pixela API configuration
TOKEN = os.getenv("PIXELA_TOKEN")
USERNAME = os.getenv("PIXELA_USERNAME")
GRAPH_ID = "graph1"
PIXELA_ENDPOINT = "https://pixe.la/v1/users"
PIXELA_GRAPH_ENDPOINT = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs/{GRAPH_ID}"
PIXELA_GRAPH_URL = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs/{GRAPH_ID}.html"

# Image path
CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
LOGO_IMG = os.path.join(CURRENT_DIRECTORY, "images", "logo.png")

# HTTP request headers
headers = {"X-USER-TOKEN": TOKEN}


def open_browser():
    """Open the Pixela graph page in a web browser."""
    webbrowser.open(PIXELA_GRAPH_URL, new=1)


def format_date(date: str) -> str:
    """Format the date to 'yyyyMMdd' which is required by the Pixela API."""
    # Parse the date string into a datetime object
    date_obj = datetime.strptime(date, "%m/%d/%y")
    # Format the datetime object into the specified string format
    formatted_date = date_obj.strftime("%Y%m%d")
    return formatted_date


def show_message(response):
    """Show an informational message box with the response status."""
    if response.ok:
        messagebox.showinfo(title="Success", message="Action completed successfully.")
    else:
        messagebox.showerror(title="Error", message=response.text)


def make_request_with_retries(request_func, url, data=None):
    """Make a request and retry until a 200 OK status code is received or a maximum number of retries is reached."""
    max_retries = 5  # Set a maximum number of retries to prevent infinite loops
    retries = 0
    while retries < max_retries:
        if data:
            response = request_func(url=url, json=data, headers=headers)
        else:
            response = request_func(url=url, headers=headers)

        if response.status_code == 200:
            return response
        else:
            retries += 1
            time.sleep(
                2
            )  # Wait for 2 seconds before retrying to avoid hammering the server
            print(
                f"Request failed with status {response.status_code}. Retrying {retries}/{max_retries}..."
            )

    return response  # Return the last response after exhausting retries


def add_pixel():
    """Add a new pixel to the Pixela graph with the given date and quantity."""
    date = format_date(cal.get_date())
    quantity = user_input.get()

    pixel_data = {"date": date, "quantity": quantity}

    response = make_request_with_retries(
        requests.post, PIXELA_GRAPH_ENDPOINT, pixel_data
    )
    user_input.delete(0, 'end')
    show_message(response)


def delete_pixel():
    """Delete the pixel from the Pixela graph corresponding to the selected date."""
    date = format_date(cal.get_date())
    response = make_request_with_retries(
        requests.delete, f"{PIXELA_GRAPH_ENDPOINT}/{date}"
    )
    show_message(response)


def update_pixel():
    """Update the pixel on the Pixela graph with the new quantity."""
    date = format_date(cal.get_date())
    quantity = user_input.get()

    pixel_data = {"quantity": quantity}

    response = make_request_with_retries(
        requests.put, f"{PIXELA_GRAPH_ENDPOINT}/{date}", pixel_data
    )
    user_input.delete(0, 'end')
    show_message(response)


# Initialize the main application window
window = Tk()
window.title("Gym Journey")
window.iconphoto(
    True, PhotoImage(file=LOGO_IMG)
)  # Ensure this path points to your icon file
window.resizable(width=False, height=False)
window.config(pady=20, padx=20)

# Calendar widget for date selection
cal = Calendar(
    window,
    selectmode='day',
    year=datetime.now().year,
    month=datetime.now().month,
    day=datetime.now().day,
)
cal.grid(row=0, column=0, columnspan=4)

# Label and entry for user input of quantity
units_label = Label(window, text="Hours/Day:")
units_label.grid(row=1, column=0, columnspan=2, pady=10, sticky="e")
user_input = Entry(window, width=10)
user_input.grid(row=1, column=2, sticky="w")

# Buttons for adding, updating, and deleting pixels, and for opening the Pixela graph
add_button = Button(window, text="Add", command=add_pixel)
add_button.grid(row=2, column=0, pady=10)
update_button = Button(window, text="Update", command=update_pixel)
update_button.grid(row=2, column=1, pady=10, sticky="w")
delete_button = Button(window, text="Delete", command=delete_pixel)
delete_button.grid(row=2, column=2, pady=10, sticky="w")
link_button = Button(window, text="Show\nJourney", command=open_browser)
link_button.grid(row=2, column=3)

# Run the application
window.mainloop()
