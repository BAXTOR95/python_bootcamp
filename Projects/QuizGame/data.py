from urllib.request import urlopen
import json

default_data = [
    {"text": "A slug's blood is green.", "answer": "True"},
    {"text": "The loudest animal is the African Elephant.", "answer": "False"},
    {"text": "Approximately one quarter of human bones are in the feet.", "answer": "True"},
    {"text": "The total surface area of a human lungs is the size of a football pitch.", "answer": "True"},
    {"text": "In West Virginia, USA, if you accidentally hit an animal with your car, "
             "you are free to take it home to eat.", "answer": "True"},
    {"text": "In London, UK, if you happen to die in the House of Parliament, "
             "you are entitled to a state funeral.", "answer": "False"},
    {"text": "It is illegal to pee in the Ocean in Portugal.", "answer": "True"},
    {"text": "You can lead a cow down stairs but not up stairs.", "answer": "False"},
    {"text": "Google was originally called 'Backrub'.", "answer": "True"},
    {"text": "Buzz Aldrin's mother's maiden name was 'Moon'.", "answer": "True"},
    {"text": "No piece of square dry paper can be folded in half more than 7 times.",
        "answer": "False"},
    {"text": "A few ounces of chocolate can kill a small dog.", "answer": "True"}
]


def get_category():
    """Get categories from Open Trivia DB API

    Returns:
        dict: categories data
    """
    # using https://opentdb.com/api_category.php api to get available categories
    url = "https://opentdb.com/api_category.php"

    # store the response of URL
    response = urlopen(url)

    # storing the JSON response from url in data
    data_json = json.loads(response.read())

    return data_json["trivia_categories"]


def get_data():
    """Get data from Open Trivia DB API

    Returns:
        dict: questionnaire data
    """

    # Select # of Questions

    i_number_questions = int(input("Select number of questions: ") or 10)
    amount = f"amount={i_number_questions}" if i_number_questions > 0 else f"amount=10"

    # Select Category
    print("Select category from the following list:")
    category_data = get_category()
    print(f"0: Any Category.", end="\n")
    for item in category_data:
        i_number = item["id"] - 8
        i_name = item["name"]
        print(f"{i_number}: {i_name}.", end="\n")
    i_category = int(input("Option: ") or 0)
    category = f"category={i_category + 8}" if i_category in range(
        1, len(category_data)) else ""

    # Select Difficulty
    i_difficulty = input(
        "Select difficulty: (easy, medium, hard): ").lower() or ""
    difficulty = f"difficulty={i_difficulty}" if i_difficulty in (
        "easy", "medium", "hard") else ""

    # using https://opentdb.com/api_config.php api to get new dataset of questions
    url = f"https://opentdb.com/api.php?{amount}&{category}&{difficulty}&type=boolean"

    # store the response of URL
    response = urlopen(url)

    # storing the JSON response from url in data
    data_json = json.loads(response.read())

    question_data = []

    if data_json["response_code"] == 0:
        questionnaire = data_json["results"]
        for question in questionnaire:
            question_data.append({
                "text": question["question"],
                "answer": question["correct_answer"]
            })
    elif data_json["response_code"] == 1:
        print("Could not return results. There are not enough questions for your query.")
        print("Using default data...")
        question_data = default_data
    else:
        print("Invalid call. Using default data...")
        question_data = default_data

    return question_data
