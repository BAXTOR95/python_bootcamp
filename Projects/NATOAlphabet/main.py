import pandas
import string

# Load the CSV into a DataFrame
nato_data = pandas.read_csv("nato_phonetic_alphabet.csv")

# Convert the DataFrame into a dictionary
phonetic_dict = dict(zip(nato_data['letter'], nato_data['code']))


# Function to convert a word into its phonetic code
def word_to_phonetic(word):
    return [
        phonetic_dict[letter.upper()]
        for letter in word
        if letter.upper() in phonetic_dict
    ]


def input_is_only_letters(user_input):
    # Check if every character in the user_input is a letter
    return all(char in string.ascii_letters for char in user_input)


while True:
    try:
        # Get user input
        user_word = input("Enter a word: ")
        print(user_word)
        if not input_is_only_letters(user_word):
            raise ValueError("Sorry, only letters in the alphabet please.")
        else:
            # Convert the word to its phonetic code
            phonetic_code = word_to_phonetic(user_word)
            print(phonetic_code)
            break
    except ValueError as e:
        print(e)
