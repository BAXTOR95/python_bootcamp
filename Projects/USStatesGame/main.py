import turtle
import pandas as pd
from PIL import Image
import sys
from pathlib import Path

# Get the parent directory of the current script
parent_dir = Path(__file__).resolve().parent.parent
# Add the parent directory to sys.path
sys.path.append(str(parent_dir))
# Import custom module
from Tools.main import ask_quit

from state_label import StateLabel

image = "blank_states_img.gif"  # Image Path

# Open the image to find its size
img = Image.open(image)
width, height = img.size

# Screen setup
screen = turtle.Screen()
screen.setup(width, height)
screen.title("U.S. States Game")
screen.addshape(image)
turtle.shape(image)

# Import Data Source
data = pd.read_csv("50_states.csv")

correct_states = []  # List of correct answers
states_quantity = len(data)


def search_state_in_df(state):
    """Searches the state in the dataframe

    Args:
        state (string): state inserted by the user
    """
    # Normalize state
    state = state.title()

    # Check if the word has already been found
    if state in correct_states:
        print(f"{state} already found, no need to type it again.")
        return

    # Search in DataFrame
    # Creating a boolean series
    state_found = data["state"] == state

    # Filtering the DataFrame
    filtered_data = data[state_found]

    # Check if the state exists
    if not filtered_data.empty:
        for index, row in filtered_data.iterrows():
            x = row['x']
            y = row['y']
            StateLabel(state, x, y)  # Creates the state label and places it in map
        # Add the word to the list of found words
        correct_states.append(state)
    else:
        print(f"{state} is not a US State!")


game_is_on = True
while game_is_on:
    correct_states_count = len(correct_states)
    if correct_states_count == 50:
        print("You Won!")
        game_is_on = False
        screen.exitonclick()
    else:
        answer_state = screen.textinput(
            title=f"{correct_states_count}/{states_quantity} States Correct",
            prompt="What's another state's name?",
        )
        # Check if user clicked 'Cancel'
        if answer_state is None:
            game_is_on = not ask_quit()
        else:
            search_state_in_df(answer_state)

# DataFrame from correct states
df_correct_states = pd.DataFrame(correct_states, columns=["state"])

# Find states that are not in the correct_states
states_not_found = data[~data["state"].isin(df_correct_states["state"])]["state"]

# Export to CSV
states_not_found.to_csv('states_not_found.csv', index=False, header=False)

# # Get mouse coordinates on click
# def get_mouse_click_coor(x, y):
#     print(x, y)

# turtle.onscreenclick(get_mouse_click_coor)
# turtle.mainloop()
