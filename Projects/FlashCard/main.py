from tkinter import *
from PIL import Image
import random
import pygame
import pandas as pd

# -------------------------------- CONSTANTS -------------------------------- #
BACKGROUND_COLOR = "#B1DDC6"
WRONG_IMG = "./images/wrong.png"
RIGHT_IMG = "./images/right.png"
CARD_BACK_IMG = "./images/card_back.png"
CARD_FRONT_IMG = "./images/card_front.png"
FONT_NAME = "Ariel"
DEFAULT_DATA_PATH = "./data/english_words.csv"
SAVED_DATA_PATH = './data/words_to_learn.csv'
CARD_FLIP_SOUND = './sounds/card_flip.wav'
CARD_SLIDE_SOUND = './sounds/card_slide.wav'
CORRECT_SOUND = './sounds/correct.wav'
WRONG_SOUND = './sounds/wrong.wav'
ORIGINAL_LANGUAGE = 'English'
TRANSLATED_LANGUAGE = 'Spanish'
DELAY = 3000

# -------------------------------- VARIABLES -------------------------------- #
timer = None
current_word = ""
word_list = []


# ---------------------------- OTHER FUNCTIONS ------------------------------ #
def play_sound(sound_path):
    pygame.mixer.init()
    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play()


def starts_delay(delay):
    global timer
    timer = window.after(delay)


def resets_delay():
    if timer:
        window.after_cancel(timer)  # Stops timer


# ---------------------------- DATA FUNCTIONS ------------------------------ #
def get_data():
    # Function to get the initial data
    global word_list
    try:
        data = pd.read_csv(SAVED_DATA_PATH)
    except FileNotFoundError:
        data = pd.read_csv(DEFAULT_DATA_PATH)
    # End Try
    finally:
        word_list = data.to_dict(orient="records")


def remove_word_pair():
    # Function to remove a word pair
    global word_list
    for word_pair in word_list:
        if word_pair[ORIGINAL_LANGUAGE] == current_word:
            word_list.remove(word_pair)


def update_data():
    remove_word_pair()

    # Convert to DataFrame
    df = pd.DataFrame(word_list)

    # Save to CSV
    df.to_csv('./data/words_to_learn.csv', index=False)


# --------------------------- CREATE FLASH CARD ----------------------------- #
def flip_card(translated_word):
    play_sound(CARD_FLIP_SOUND)
    canvas.itemconfig(canvas_image, image=card_back_img)
    canvas.itemconfig(language_text, text=TRANSLATED_LANGUAGE, fill="white")
    canvas.itemconfig(word_text, text=translated_word.capitalize(), fill="white")
    canvas.update()


def set_card(original_word):
    global current_word
    play_sound(CARD_SLIDE_SOUND)
    current_word = original_word
    canvas.itemconfig(canvas_image, image=card_front_img)
    canvas.itemconfig(language_text, text=ORIGINAL_LANGUAGE, fill="black")
    canvas.itemconfig(word_text, text=original_word.capitalize(), fill="black")
    canvas.update()


def pick_new_word():
    resets_delay()

    word_pair = random.choice(word_list)  # Randomly pick a dictionary from the list

    original_word = word_pair[ORIGINAL_LANGUAGE]  # Get the Original word
    translated_word = word_pair[
        TRANSLATED_LANGUAGE
    ]  # Get the corresponding translated word

    set_card(original_word)

    starts_delay(DELAY)

    flip_card(translated_word)


# ------------------------- BUTTONS FUNCTIONALITY --------------------------- #
def correct():
    play_sound(CORRECT_SOUND)
    starts_delay(1000)
    update_data()
    pick_new_word()


def wrong():
    play_sound(WRONG_SOUND)
    starts_delay(1000)
    pick_new_word()


# ------------------------------ INITIAL SETUP ------------------------------ #
get_data()

# ------------------------------- UI SETUP ---------------------------------- #

# Window Setup
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
# Set the window icon
window.iconbitmap('./images/logo.ico')

# Open the card image to find its size
img = Image.open(CARD_BACK_IMG)
img_width, img_height = img.size
# Get images
card_back_img = PhotoImage(file=CARD_BACK_IMG)
card_front_img = PhotoImage(file=CARD_FRONT_IMG)
wrong_img = PhotoImage(file=WRONG_IMG)
right_img = PhotoImage(file=RIGHT_IMG)

# Canvas setup
canvas = Canvas(
    width=img_width, height=img_height, bg=BACKGROUND_COLOR, highlightthickness=0
)
# Background Image
canvas_image = canvas.create_image(400, 263, image=card_front_img)
# Texts
language_text = canvas.create_text(
    400, 150, text=ORIGINAL_LANGUAGE, fill="black", font=(FONT_NAME, 40, "italic")
)
word_text = canvas.create_text(
    400, 263, text="", fill="black", font=(FONT_NAME, 60, "bold")
)
canvas.grid(column=0, row=0, columnspan=2, sticky="EW")

# Buttons
wrong_btn = Button(image=wrong_img, borderwidth=0, highlightthickness=0, command=wrong)
wrong_btn.grid(column=0, row=1)
right_btn = Button(
    image=right_img, borderwidth=0, highlightthickness=0, command=correct
)
right_btn.grid(column=1, row=1)

pick_new_word()

window.mainloop()
