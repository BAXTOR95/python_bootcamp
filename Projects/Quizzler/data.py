from tkinter import messagebox
from api import fetch_trivia_questions
from validation import validate_trivia_parameters
import html
import json


def load_default_trivia_data(file_path: str) -> list:
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading default trivia data: {e}")
        return []


def get_trivia_data(questions: int, category: int, difficulty: str) -> list:
    # Load default trivia data from a file
    default_data = load_default_trivia_data('default_trivia_questions.json')

    if not validate_trivia_parameters(questions, category, difficulty):
        return default_data

    data_json = fetch_trivia_questions(questions, category, difficulty)
    if not data_json:
        messagebox.showerror(
            "Error", "Failed to fetch data from API. Using default data."
        )
        return default_data

    if data_json["response_code"] == 1:
        messagebox.showerror(
            "Not enough data", "Not enough data for your request. Using default data."
        )
        return default_data
    elif data_json["response_code"] not in (0, 1):
        messagebox.showerror("Error", "API Error. Using default data.")
        return default_data

    return [
        {
            "text": html.unescape(question["question"]),
            "answer": question["correct_answer"],
        }
        for question in data_json["results"]
    ]
