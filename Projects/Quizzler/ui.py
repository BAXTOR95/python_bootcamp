import os
from tkinter import *
from data import get_data, get_category
from question_model import Question
from quiz_brain import QuizBrain
from tkinter import messagebox


class QuizInterface:
    THEME_COLOR = "#375362"
    FONT_NAME = "Arial"
    CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
    TRUE_IMG = os.path.join(CURRENT_DIRECTORY, "images", "true.png")
    FALSE_IMG = os.path.join(CURRENT_DIRECTORY, "images", "false.png")
    BACK_IMG = os.path.join(CURRENT_DIRECTORY, "images", "back.png")

    def __init__(self) -> None:
        self.window = Tk()
        self.window.title("Quizzler")
        self.window.config(padx=20, pady=20, bg=self.THEME_COLOR)

        self.timer = None
        self.validate_only_numbers = (self.window.register(self._only_numbers), '%P')
        self.categories = get_category()
        self.n_questions = 0
        self.category_selected = 0
        self.difficulty = None
        self.question_bank = []
        self.quiz = None
        self.current_trivia = ""
        self.selection_screen = None
        self.n_questions_spbx = None
        self.categories_lst = None
        self.radio_state = None
        self.trivia_canvas = None
        self.trivia_text = None
        self.true_img = None
        self.false_img = None
        self.back_img = None

        # Setup for the selection screen
        self.setup_selection_screen()
        # Initially hiding the game screen until it's set up
        self.game_screen = None

    def _only_numbers(self, P):
        if P.isdigit():
            num = int(P)
            if 0 <= num <= 50:
                return True
        elif P == "":
            # Allow empty field for backspace/delete
            return True
        return False

    def _starts_delay(self, delay):
        self.timer = self.window.after(delay)

    def _resets_delay(self):
        if self.timer:
            self.window.after_cancel(self.timer)  # Stops timer

    def _set_question_bank(self):
        self.n_questions = int(self.n_questions_spbx.get())
        self.category_selected = int(self.categories_lst.curselection()[0])
        self.difficulty = self.radio_state.get()

        for question in get_data(
            self.n_questions, self.category_selected, self.difficulty
        ):  # looping through question_data
            self.question_bank.append(Question(question["text"], question["answer"]))

    def _update_score(self):
        self.score_lbl.config(
            text=f"Score: {self.quiz.score}/{self.quiz.question_number+1}"
        )

    def _reset_canvas(self):
        self.trivia_canvas.config(bg='white')
        self.trivia_canvas.itemconfig(
            self.trivia_text, text=self.current_trivia, fill="black"
        )
        self.trivia_canvas.update()

    def _reset_game_screen(self):
        self.question_bank = []
        self.current_trivia = ""
        self._reset_canvas()
        self.score_lbl.config(text="Score: 0/0")

    def _correct_answer(self):
        self.trivia_canvas.config(bg='green')

    def _incorrect_answer(self):
        self.trivia_canvas.config(bg='red')

    def _check_answer(self, answer):
        if self.quiz.still_has_questions():
            if self.quiz.check_answer(answer):
                self._correct_answer()
            else:
                self._incorrect_answer()
            self.trivia_canvas.itemconfig(self.trivia_text, fill="white")
            self._update_score()
            self.trivia_canvas.update()
            self._starts_delay(1000)
            if not self.quiz.on_last_question():
                self._next_question()
            else:
                messagebox.showinfo(
                    "Quiz Ended",
                    f"There are no more questions.\nFinal Score: {self.score_lbl.cget('text')}",
                )
                self.back_to_selection()

    def _next_question(self):
        self._reset_canvas()
        self.current_trivia = self.quiz.next_question()
        self._reset_canvas()

    def _show_selection_screen(self):
        self.selection_screen.grid(row=0, column=0)

    def setup_selection_screen(self):
        self.selection_screen = Frame(self.window, padx=20, pady=20)
        # Question selector
        n_questions_lbl = Label(
            self.selection_screen, text="Select number of questions:"
        )
        n_questions_lbl.grid(row=0, column=0)
        self.n_questions_spbx = Spinbox(
            self.selection_screen,
            from_=0,
            to=50,
            value=10,
            width=5,
            validate="key",
            validatecommand=self.validate_only_numbers,
        )
        self.n_questions_spbx.grid(row=0, column=1)

        # Categories selector
        n_categories_lbl = Label(
            self.selection_screen, text="Select category from the following list:"
        )
        n_categories_lbl.grid(row=1, column=0)
        self.categories_lst = Listbox(self.selection_screen, height=5)
        for category in self.categories:
            self.categories_lst.insert(category["id"], category["name"])
        self.categories_lst.selection_set(0)
        self.categories_lst.grid(row=1, column=1)

        # Difficulty selector
        n_difficulty_lbl = Label(self.selection_screen, text="Choose the difficulty:")
        n_difficulty_lbl.grid(row=2, column=0, rowspan=3)
        self.radio_state = StringVar(value="easy")
        easy_rbtn = Radiobutton(
            self.selection_screen,
            text="Easy",
            value="easy",
            variable=self.radio_state,
        )
        easy_rbtn.grid(row=2, column=1)
        medium_rbtn = Radiobutton(
            self.selection_screen,
            text="Medium",
            value="medium",
            variable=self.radio_state,
        )
        medium_rbtn.grid(row=3, column=1)
        hard_rbtn = Radiobutton(
            self.selection_screen,
            text="Hard",
            value="hard",
            variable=self.radio_state,
        )
        hard_rbtn.grid(row=4, column=1)

        # Play Button
        play_button = Button(
            self.selection_screen, text="Play", command=self.start_game
        )
        play_button.grid(column=0, row=5, columnspan=2, sticky="EW")

    def setup_game_screen(self):
        self.game_screen = Frame(self.window, padx=20, pady=20)

        # Back button
        self.back_img = PhotoImage(file=self.BACK_IMG)
        back_button = Button(
            self.game_screen,
            image=self.back_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.back_to_selection,
        )
        back_button.grid(row=0, column=0, sticky="EW")

        # Score label
        self.score_lbl = Label(
            self.game_screen,
            text=f"Score: {self.quiz.score}/{self.quiz.question_number+1}",
        )
        self.score_lbl.grid(row=0, column=1)

        # Trivia Canvas
        self.trivia_canvas = Canvas(self.game_screen, width=300, height=250, bg="white")
        self.trivia_text = self.trivia_canvas.create_text(
            150,
            125,
            text=self.current_trivia,
            font=(self.FONT_NAME, 20, "italic"),
            width=280,
            fill="black",
        )
        self.trivia_canvas.grid(row=1, column=0, columnspan=2, sticky="EW")

        # Choice Buttons
        self.true_img = PhotoImage(file=self.TRUE_IMG)
        true_btn = Button(
            self.game_screen,
            image=self.true_img,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self._check_answer("True"),
        )
        true_btn.grid(row=2, column=0, sticky="EW")

        self.false_img = PhotoImage(file=self.FALSE_IMG)
        false_btn = Button(
            self.game_screen,
            image=self.false_img,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self._check_answer("False"),
        )
        false_btn.grid(row=2, column=1, sticky="EW")

    def start_game(self):
        # Hide selection screen and setup game screen
        self._set_question_bank()
        self.quiz = QuizBrain(self.question_bank)
        self.current_trivia = self.quiz.current_question()
        self.selection_screen.grid_forget()
        if not self.game_screen:
            self.setup_game_screen()
        self._reset_canvas()
        self.game_screen.grid(row=0, column=0)

    def back_to_selection(self):
        # Hide game screen and show selection screen
        self._reset_game_screen()
        self.game_screen.grid_forget()
        self._show_selection_screen()

    def run(self):
        self._show_selection_screen()
        self.window.mainloop()


if __name__ == "__main__":
    quiz_app = QuizInterface()
    quiz_app.run()
