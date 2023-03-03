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


def get_data():
    """Get data from Open Trivia DB API

    Returns:
        dict: questionnaire data
    """
    # using https://opentdb.com/api_config.php api to get new dataset of questions
    url = "https://opentdb.com/api.php?amount=10&category=18&difficulty=easy&type=boolean"

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
    else:
        question_data = default_data

    return question_data
