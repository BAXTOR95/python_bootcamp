# Morse code dictionary
morse_code_dict = {
    'A': '.-',
    'B': '-...',
    'C': '-.-.',
    'D': '-..',
    'E': '.',
    'F': '..-.',
    'G': '--.',
    'H': '....',
    'I': '..',
    'J': '.---',
    'K': '-.-',
    'L': '.-..',
    'M': '--',
    'N': '-.',
    'O': '---',
    'P': '.--.',
    'Q': '--.-',
    'R': '.-.',
    'S': '...',
    'T': '-',
    'U': '..-',
    'V': '...-',
    'W': '.--',
    'X': '-..-',
    'Y': '-.--',
    'Z': '--..',
    '1': '.----',
    '2': '..---',
    '3': '...--',
    '4': '....-',
    '5': '.....',
    '6': '-....',
    '7': '--...',
    '8': '---..',
    '9': '----.',
    '0': '-----',
    ' ': '/',
}


def normalize_spanish_characters(text):
    """
    Normalizes Spanish accented characters to their unaccented equivalent,
    focusing on uppercase since the text will be converted to uppercase
    before Morse code conversion.

    Args:
        text (str): The text containing potentially Spanish accented characters.

    Returns:
        str: The normalized text, all in uppercase.
    """
    normalization_dict = {
        'Á': 'A',
        'É': 'E',
        'Í': 'I',
        'Ó': 'O',
        'Ú': 'U',
        'Ñ': 'N',  # Only handling uppercase since text will be converted to uppercase
    }
    return ''.join(normalization_dict.get(char, char) for char in text.upper())


def text_to_morse(text):
    """
    Converts a given text into Morse code, handling Spanish accented characters
    and converting all characters to uppercase as part of the normalization.

    Args:
        text (str): The text to be converted.

    Returns:
        str: The Morse code representation of the input text.
    """
    normalized_text = normalize_spanish_characters(text)
    morse_code = ''
    for char in normalized_text.upper():
        if char in morse_code_dict:
            morse_code += morse_code_dict[char] + ' '
        elif char in ",.;¿?!¡":  # Add basic punctuation handling
            morse_code += ''
        else:
            morse_code += '? '  # Indicates an unrecognized character
    return morse_code.strip()


# Main program loop
while True:
    text = input("Enter text to convert to Morse Code (or type 'quit' to exit): ")
    if text.lower() == 'quit':
        print("Exiting program...")
        break
    print("Morse Code:", text_to_morse(text))
