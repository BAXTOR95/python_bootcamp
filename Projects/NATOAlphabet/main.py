import pandas

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


# Get user input
user_word = input("Enter a word: ")

# Convert the word to its phonetic code
phonetic_code = word_to_phonetic(user_word)

print(phonetic_code)
