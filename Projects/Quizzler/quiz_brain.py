from question_model import Question


class QuizBrain:
    """Class for Quiz Brain object"""

    def __init__(self, question_list: list[Question]):
        self.question_number = 0
        self.question_list = question_list
        self.score = 0

    def still_has_questions(self):
        return self.question_number < len(self.question_list)

    def on_last_question(self):
        return self.question_number == len(self.question_list) - 1

    def normalize_answer(self, answer: str):
        return answer.lower()[0]

    def check_answer(self, answer: str):
        c_question = self.question_list[self.question_number - 1]
        if self.normalize_answer(c_question.answer) == self.normalize_answer(answer):
            self.score += 1
            print("You got it right!")
            return True
        else:
            print("That's wrong...")
            print(f"The correct answer was: {c_question.answer}.\n")
            return False

    def current_question(self):
        return self.question_list[self.question_number].text

    def next_question(self):
        self.question_number += 1
        return self.current_question()
