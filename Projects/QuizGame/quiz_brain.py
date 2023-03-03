from question_model import Question


class QuizBrain:
    """Class for Quiz Brain object
    """

    def __init__(self, question_list: list[Question]):
        self.question_number = 0
        self.question_list = question_list
        self.score = 0

    def still_has_questions(self):
        return self.question_number < len(self.question_list)

    def normalize_answer(self, answer: str):
        return answer.lower()[0]

    def check_answer(self, answer: str, c_answer: str):
        if self.normalize_answer(c_answer) == self.normalize_answer(answer):
            self.score += 1
            print("You got it right!")
        else:
            print("That's wrong...")

        print(f"The correct answer was: {c_answer}.")
        print(f"Your current score is: {self.score}/{self.question_number}.")
        print("\n")

    def next_question(self):
        c_question = self.question_list[self.question_number]
        self.question_number += 1
        answer = input(f"Q.{self.question_number}: {c_question.text} "
                       f"(True/False)?: ") or " "
        self.check_answer(answer, c_question.answer)
