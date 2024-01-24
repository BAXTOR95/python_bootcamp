# from question_model import Question
# from data import get_data
# from quiz_brain import QuizBrain
from ui import QuizInterface

# question_bank = []
# for question in get_data():  # looping through question_data
#     question_bank.append(Question(question["text"], question["answer"]))

# quiz = QuizBrain(question_bank)
quiz_ui = QuizInterface()

# while quiz.still_has_questions():
#     quiz.next_question()

# print("You've completed the quiz!")
# print(f"Your final score was: {quiz.score}/{quiz.question_number}.")
