import requests
import html
from tkinter import messagebox

default_data = [
    {"text": "A slug's blood is green.", "answer": "True"},
    {"text": "The loudest animal is the African Elephant.", "answer": "False"},
    {
        "text": "Approximately one quarter of human bones are in the feet.",
        "answer": "True",
    },
    {
        "text": "The total surface area of a human lungs is the size of a football pitch.",
        "answer": "True",
    },
    {
        "text": "In West Virginia, USA, if you accidentally hit an animal with your car, "
        "you are free to take it home to eat.",
        "answer": "True",
    },
    {
        "text": "In London, UK, if you happen to die in the House of Parliament, "
        "you are entitled to a state funeral.",
        "answer": "False",
    },
    {"text": "It is illegal to pee in the Ocean in Portugal.", "answer": "True"},
    {"text": "You can lead a cow down stairs but not up stairs.", "answer": "False"},
    {"text": "Google was originally called 'Backrub'.", "answer": "True"},
    {"text": "Buzz Aldrin's mother's maiden name was 'Moon'.", "answer": "True"},
    {
        "text": "No piece of square dry paper can be folded in half more than 7 times.",
        "answer": "False",
    },
    {"text": "A few ounces of chocolate can kill a small dog.", "answer": "True"},
]


def get_category():
    """Get categories from Open Trivia DB API

    Returns:
        dict: categories data
    """
    # using https://opentdb.com/api_category.php api to get available categories
    url = "https://opentdb.com/api_category.php"

    # store the response of URL
    response = requests.get(url)
    response.raise_for_status()

    # storing the JSON response from url in data
    data_json = response.json()
    default_data = [{"id": 0, "name": "Any Category"}]

    return default_data + data_json["trivia_categories"]


def get_data(p_questions, p_category, p_difficulty):
    """Get data from Open Trivia DB API

    Returns:
        dict: questionnaire data
    """

    # Set # of Questions
    amount = f"amount={p_questions}" if p_questions > 0 else f"amount=10"

    # Set Category
    category = f"category={p_category}"

    # Set Difficulty
    difficulty = f"difficulty={p_difficulty}"

    # using https://opentdb.com/api_config.php api to get new dataset of questions
    url = f"https://opentdb.com/api.php?{amount}&{category}&{difficulty}&type=boolean"

    question_data = []

    try:
        # store the response of URL
        response = requests.get(url)
        response.raise_for_status()

        # storing the JSON response from url in data
        data_json = response.json()

        if data_json["response_code"] == 0:
            questionnaire = data_json["results"]
            for question in questionnaire:
                question_data.append(
                    {
                        "text": html.unescape(question["question"]),
                        "answer": question["correct_answer"],
                    }
                )
        elif data_json["response_code"] == 1:
            messagebox.showerror(
                "Could not get results",
                "There are not enough questions for your query.\nUsing default data...",
            )
            question_data = default_data
        else:
            messagebox.showerror(
                "Could not get results",
                "Invalid call.\nUsing default data...",
            )
            question_data = default_data

    except Exception as e:
        messagebox.showerror(
            "Could not get results",
            "Invalid call.\nUsing default data...",
        )
        question_data = default_data

    finally:
        return question_data
