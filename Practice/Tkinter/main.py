# import tkinter as tk
from tkinter import *


def button_clicked():
    # print("I got clicked")
    # my_label.config(text="Button got clicked")
    my_label.config(text=input.get())


window = Tk()
window.title("My First GUI Program")
window.minsize(width=500, height=300)
window.config(padx=100, pady=200)

# Label

my_label = Label(text="I Am a Label", font=("Arial", 24, "bold"))
my_label["text"] = "New Text"
my_label.config(text="New Text")
# my_label.pack(side="left")
# my_label.place(x=100, y=200)
my_label.grid(column=0, row=0)
my_label.config(padx=50, pady=50)

# Button

button = Button(text="Click Me", command=button_clicked)
# button.pack(side="left")
button.grid(column=1, row=1)

button2 = Button(text="Click Me Too!", command=button_clicked)
button2.grid(column=2, row=0)


# Entry

input = Entry(width=10)
# input.pack(side="left")
input.grid(column=3, row=2)

window.mainloop()
