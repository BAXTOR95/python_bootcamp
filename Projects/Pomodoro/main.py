from tkinter import *
from PIL import Image
import pygame

# ------------------------------ CONSTANTS ------------------------------- #
DARK_BLUE = "#222831"
DARK_GREY = "#393E46"
TEAL = "#00ADB5"
GREY = "#EEEEEE"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
IMAGE_PATH = "tomato.png"
CHECK_MARK = "✔"
reps = 0
timer = None


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    global reps
    reps = 0  # Reset reps
    window.after_cancel(timer)  # Resets timer
    canvas.itemconfig(timer_text, text="00:00")  # Resets timer text
    timer_label.config(text="Pomodoro", fg=DARK_BLUE)  # Resets title
    checkmk_label.config(text="")  # Resets check marks


# ---------------------------- TIMER MECHANISM --------------------------- #
def focusWindow():
    window.lift()  # Bring the window to the front
    window.attributes('-topmost', True)  # Temporarily make the window stay on top
    window.update()  # Update the window to reflect the change
    window.attributes('-topmost', False)  # Revert to normal


def play_sound():
    pygame.mixer.init()
    pygame.mixer.music.load('beep.wav')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play()


def start_timer():
    global reps
    reps += 1
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        play_sound()
        focusWindow()
        count_down(long_break_sec)
        timer_label.config(text="Break", fg=DARK_GREY)
    elif reps % 2 == 0:
        play_sound()
        focusWindow()
        count_down(short_break_sec)
        timer_label.config(text="Break", fg=DARK_BLUE)
    else:
        focusWindow()
        count_down(work_sec)
        timer_label.config(text="Work", fg=TEAL)


# ------------------------- COUNTDOWN MECHANISM -------------------------- #
def count_down(count):
    # Calculate minutes and seconds
    minutes = count // 60
    seconds = count % 60

    # Format as "MM:SS"
    formatted_time = f"{minutes:02}:{seconds:02}"

    canvas.itemconfig(timer_text, text=formatted_time)
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        marks = ""
        for _ in range(reps // 2):
            marks += CHECK_MARK
        checkmk_label.config(text=marks)


# ------------------------------ UI SETUP -------------------------------- #

# Window Setup
window = Tk()
window.title("Pomodoro")
window.config(padx=50, pady=25, bg=GREY)
# Set the window icon
window.iconbitmap('tomato.ico')

# Open the image to find its size
img = Image.open(IMAGE_PATH)
img_width, img_height = img.size
tomato_img = PhotoImage(file=IMAGE_PATH)

# Canvas setup
canvas = Canvas(width=img_width, height=img_height, bg=GREY, highlightthickness=0)
# Background Image
canvas.create_image(100, 112, image=tomato_img)
# Timer
timer_text = canvas.create_text(
    100, 120, text="00:00", fill="white", font=(FONT_NAME, 30, "bold")
)
canvas.grid(column=1, row=1)

# Title
timer_label = Label(
    text="Pomodoro", fg=DARK_BLUE, bg=GREY, font=(FONT_NAME, 30, "bold")
)
timer_label.grid(column=1, row=0)

# Buttons
start_btn = Button(
    text="Start", command=start_timer, bg=DARK_GREY, fg=GREY, highlightthickness=0
)
start_btn.grid(column=0, row=1)
reset_btn = Button(
    text="Reset", command=reset_timer, bg=DARK_GREY, fg=GREY, highlightthickness=0
)
reset_btn.grid(column=2, row=1)

# Check marks
checkmk_label = Label(fg=TEAL, font=(FONT_NAME, 15, "bold"))
checkmk_label.grid(column=1, row=3)

window.mainloop()
