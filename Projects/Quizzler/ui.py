from tkinter import *
from data import get_data, get_category
from question_model import Question
from quiz_brain import QuizBrain


class QuizInterface:
    THEME_COLOR = "#375362"
    FONT_NAME = "Arial"
    TRUE_IMG = "./images/true.png"
    FALSE_IMG = "./images/false.png"
    BACK_IMG = "./images/back.png"

    def __init__(self) -> None:
        self.window = Tk()
        self.window.title("Quizzler")
        self.window.config(padx=20, pady=20, bg=self.THEME_COLOR)

        self.validate_only_numbers = (self.window.register(self._only_numbers), '%P')
        self.categories = get_category()
        self.n_questions = 0
        self.category_selected = 0
        self.difficulty = None
        self.question_bank = []
        self.quiz = None
        self.current_trivia = ""
        self.selection_screen = None
        self.game_screen = None
        self.n_questions_spbx = None
        self.categories_lst = None
        self.radio_state = None
        self.trivia_canvas = None
        self.trivia_text = None

        self.setup_selection_screen()

    def _only_numbers(P):
        if P.isdigit():
            num = int(P)
            if 0 <= num <= 50:
                return True
        elif P == "":
            # Allow empty field for backspace/delete
            return True
        return False

    def _set_question_bank(self):
        self.n_questions = self.n_questions_spbx.get()
        self.category_selected = self.categories_lst.curselection()[0]
        self.difficulty = self.radio_state.get()

        for question in get_data(
            self.n_questions, self.category_selected, self.difficulty
        ):  # looping through question_data
            self.question_bank.append(Question(question["text"], question["answer"]))

    def _true(self):
        self.quiz()

    def setup_selection_screen(self):
        self.selection_screen = Frame(self.window)
        # Question selector
        n_questions_lbl = Label(
            self.selection_screen, text="Select number of questions:"
        )
        n_questions_lbl.grid(row=0, column=0)
        self.n_questions_spbx = Spinbox(
            self.selection_screen,
            from_=0,
            to=50,
            width=5,
            validate="key",
            validatecommand=self.validate_only_numbers,
        )
        self.n_questions_spbx.grid(row=0, column=1)

        # Categories selector
        n_categories_lbl = Label(
            self.selection_screen, text="Select category from the following list:"
        )
        n_categories_lbl.grid(row=0, column=0)
        self.categories_lst = Listbox(self.selection_screen, height=5)
        for category in self.categories:
            self.categories_lst.insert(category["id"], category["name"])
        self.categories_lst.grid(row=0, column=1)

        # Difficulty selector
        n_categories_lbl = Label(self.selection_screen, text="Choose the difficulty:")
        n_categories_lbl.grid(row=0, column=0)
        self.radio_state = StringVar()
        easy_rbtn = Radiobutton(
            self.selection_screen, text="Easy", value="easy", variable=self.radio_state
        )
        easy_rbtn.grid(row=0, column=1)
        medium_rbtn = Radiobutton(
            self.selection_screen,
            text="Medium",
            value="medium",
            variable=self.radio_state,
        )
        medium_rbtn.grid(row=0, column=1)
        hard_rbtn = Radiobutton(
            self.selection_screen, text="Hard", value="hard", variable=self.radio_state
        )
        hard_rbtn.grid(row=0, column=1)

        # Play Button
        play_button = Button(
            self.selection_screen, text="Play", command=self.start_game
        )
        play_button.grid(column=0, row=1, columnspan=1, sticky="EW")

    def setup_game_screen(self):
        self.game_screen = Frame(self.window)

        # Back button
        back_img = PhotoImage(file=self.BACK_IMG)
        back_button = Button(
            self.game_screen,
            image=back_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.back_to_selection,
        )
        back_button.pack()

        # Score label
        score_lbl = Label(self.game_screen, text=f"Score: {self.quiz.score}")
        score_lbl.grid(row=0, column=1)

        # Trivia Canvas
        self.trivia_canvas = Canvas(width=300, height=250)
        self.trivia_text = self.trivia_canvas.create_text(
            150, 125, text=self.current_trivia, font=(self.FONT_NAME, 20, "italic")
        )
        self.trivia_canvas.grid(row=1, column=0, columnspan=1, sticky="EW")

        # Choice Buttons
        true_img = PhotoImage(file=self.TRUE_IMG)
        true_btn = Button(
            self.game_screen, image=true_img, borderwidth=0, highlightthickness=0
        )
        true_btn.grid(row=2, column=0)

        false_img = PhotoImage(file=self.FALSE_IMG)
        false_btn = Button(
            self.game_screen, image=false_img, borderwidth=0, highlightthickness=0
        )
        false_btn.grid(row=2, column=0)

    def start_game(self):
        # Hide selection screen and setup game screen
        self._set_question_bank()
        self.quiz = QuizBrain(self.question_bank)

        # TODO: Fix QuizBrain to accommodate the new UI changes
        # TODO: Prefill the game screen values with data from quiz
        # TODO: Add methods to change the texts in game screen when the trivia changes
        # TODO: Add methods for True and False buttons
        # TODO: Fix UI

        self.selection_screen.pack_forget()
        if not self.game_screen:
            self.setup_game_screen()
        self.game_screen.pack()

    def back_to_selection(self):
        # Hide game screen and show selection screen
        self.game_screen.pack_forget()
        self.selection_screen.pack()

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    quiz_app = QuizInterface()
    quiz_app.run()
