from tkinter import *
import requests


def get_quote():
    response = requests.get(
        url="https://api.whatdoestrumpthink.com/api/v1/quotes/random/"
    )
    response.raise_for_status()
    message = response.json()["message"]
    canvas.itemconfig(quote_text, text=message)


window = Tk()
window.title("Trump Says...")
window.config(padx=50, pady=50)

canvas = Canvas(width=300, height=414)
background_img = PhotoImage(file="background.png")
canvas.create_image(150, 207, image=background_img)
quote_text = canvas.create_text(
    150,
    207,
    text="",
    width=250,
    font=("Arial", 15, "bold"),
    fill="white",
)
canvas.grid(row=0, column=0)

trump_img = PhotoImage(file="trump.png")
trump_button = Button(
    image=trump_img, highlightthickness=0, borderwidth=0, command=get_quote
)
trump_button.grid(row=1, column=0)

get_quote()
window.mainloop()
