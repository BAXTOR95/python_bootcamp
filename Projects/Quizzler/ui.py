import os
import pygame
from tkinter import *
from data import get_trivia_data
from question_model import Question
from quiz_brain import QuizBrain
from tkinter import messagebox
from api import fetch_categories

# Global constants for theming and file paths
THEME_COLOR = "#375362"
FONT_NAME = "Arial"
CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
TRUE_IMG = os.path.join(CURRENT_DIRECTORY, "images", "true.png")
FALSE_IMG = os.path.join(CURRENT_DIRECTORY, "images", "false.png")
BACK_IMG = os.path.join(CURRENT_DIRECTORY, "images", "back.png")
CORRECT_SOUND = os.path.join(CURRENT_DIRECTORY, "sounds", "correct.wav")
WRONG_SOUND = os.path.join(CURRENT_DIRECTORY, "sounds", "wrong.wav")


class QuizInterface:
    """A class to represent the quiz interface using Tkinter."""

    def __init__(self) -> None:
        """Initialize the QuizInterface with default values and setup the selection screen."""
        self.window = Tk()
        self.window.title("Quizzler")
        self.window.config(padx=20, pady=10, bg=THEME_COLOR)

        self.timer = None
        self.validate_only_numbers = (self.window.register(self._only_numbers), '%P')
        self.categories = fetch_categories()
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
        self.true_img = self._load_image(TRUE_IMG)
        self.false_img = self._load_image(FALSE_IMG)
        self.back_img = self._load_image(BACK_IMG)

        # Initially hiding the game screen until it's set up
        self.game_screen = None
        # Setup for the selection screen
        self.setup_selection_screen()

    def _only_numbers(self, P):
        """Ensure that the entry widget accepts only numeric input."""
        if P.isdigit():
            num = int(P)
            if 0 <= num <= 50:
                return True
        elif P == "":
            # Allow empty field for backspace/delete
            return True
        return False

    def _start_delay_timer(self, delay: int):
        """Starts a delay timer for transitioning to the next question."""
        self.timer = self.window.after(delay)

    def _set_question_bank(self):
        """Sets up the question bank from the trivia data."""
        self.n_questions = int(self.n_questions_spbx.get())
        self.category_selected = int(self.categories_lst.curselection()[0])
        self.difficulty = self.radio_state.get()

        for question in get_trivia_data(
            self.n_questions, self.category_selected, self.difficulty
        ):  # looping through question_data
            self.question_bank.append(Question(question["text"], question["answer"]))

    def _get_score_string(self):
        """Returns the formatted score values"""
        return f"{self.quiz.score}/{self.quiz.question_number+1}"

    def _update_score_label(self):
        """Updates the score label with the current score."""
        self.score_lbl.config(text=f"Score: {self._get_score_string()}")

    def _reset_trivia_canvas(self):
        """Resets the trivia canvas to its default state."""
        self.trivia_canvas.config(bg='white')
        self.trivia_canvas.itemconfig(
            self.trivia_text, text=self.current_trivia, fill="black"
        )
        self.trivia_canvas.update()

    def _reset_game_screen(self):
        """Resets the game screen to its initial state."""
        self.question_bank = []
        self.current_trivia = ""
        self._reset_trivia_canvas()
        self.score_lbl.config(text="Score: 0/0")

    def _show_answer_feedback(self, bg):
        """Updates the canvas to show feedback for a correct answer."""
        self.trivia_canvas.config(bg=bg)
        self.trivia_canvas.itemconfig(self.trivia_text, fill="white")
        self.trivia_canvas.update()

    def _check_answer(self, answer):
        """Checks the user's answer and updates the UI accordingly."""
        is_correct = self.quiz.check_answer(answer)
        self._update_feedback(is_correct)
        self._update_score_label()
        self._prepare_next_question()

    def _update_feedback(self, is_correct):
        """Updates the UI based on whether the answer was correct."""
        if is_correct:
            self.play_sound(CORRECT_SOUND)
            self._show_answer_feedback("green")
        else:
            self.play_sound(WRONG_SOUND)
            self._show_answer_feedback("red")

    def _prepare_next_question(self):
        """Prepares the UI for the next question or ends the quiz."""
        if self.quiz.still_has_questions() and not self.quiz.on_last_question():
            self._start_delay_timer(1000)
            self._next_question()
        else:
            self._end_quiz()

    def _end_quiz(self):
        """Ends the quiz and shows the final score."""
        messagebox.showinfo(
            "Quiz Ended",
            f"There are no more questions.\nFinal Score: {self._get_score_string()}",
        )
        self.back_to_selection()

    def _format_question(self, question):
        """Formats the question by adding the question number at the start"""
        return f"Q.{self.quiz.question_number + 1}: {question}"

    def _next_question(self):
        """Displays the next question on the trivia canvas."""
        self.current_trivia = self._format_question(self.quiz.next_question())
        self._reset_trivia_canvas()

    def _show_selection_screen(self):
        """Displays the selection screen."""
        self.selection_screen.grid(row=0, column=0)

    def _load_image(self, image_path):
        """Loads an image from a given path and handles any loading errors."""
        try:
            return PhotoImage(file=image_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {e}")
            return None

    def _create_label(self, parent, text, row, column, **kwargs):
        """Creates a label widget with specified properties."""
        label = Label(parent, text=text, bg=THEME_COLOR, fg="white")
        label.grid(row=row, column=column, padx= 5, **kwargs)
        return label

    def _create_button(self, parent, image, command, row, column):
        """Creates a button widget with specified properties."""
        button = Button(
            parent,
            image=image,
            borderwidth=0,
            highlightthickness=0,
            command=command,
            bg=THEME_COLOR,
        )
        button.grid(row=row, column=column, sticky="EW", pady=10)
        return button

    def _create_radiobutton(self, text, value, row, column):
        """Creates a Radiobutton with common properties and grid placement."""
        radiobutton = Radiobutton(
            self.selection_screen,
            text=text,
            value=value,
            variable=self.radio_state,
            bg=THEME_COLOR,
            fg="white",
            selectcolor=THEME_COLOR,
        )
        radiobutton.grid(row=row, column=column, pady=5)
        return radiobutton

    def _validate_inputs(self):
        """Validates user inputs for number of questions, category, and difficulty."""
        if not self._is_valid_question_number():
            messagebox.showerror(
                "Input Error", "Please enter a valid number of questions (1-50)."
            )
            return False

        if not self._is_category_selected():
            messagebox.showerror("Input Error", "Please select a category.")
            return False

        # Difficulty is always valid if it's one of the radio button options
        return True

    def _is_valid_question_number(self):
        """Checks if the entered number of questions is valid."""
        try:
            num_questions = int(self.n_questions_spbx.get())
            return 1 <= num_questions <= 50
        except ValueError:
            return False

    def _is_category_selected(self):
        """Checks if a category is selected in the Listbox."""
        return bool(self.categories_lst.curselection())

    def play_sound(self, sound_path):
        pygame.mixer.init()
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()

    def setup_selection_screen(self):
        """Sets up the initial selection screen for the quiz."""
        self.selection_screen = Frame(self.window, padx=20, pady=10, bg=THEME_COLOR)
        # Question selector
        self._create_label(self.selection_screen, "Select number of questions:", 0, 0)
        self.n_questions_spbx = Spinbox(
            self.selection_screen,
            from_=0,
            to=50,
            value=10,
            width=5,
            validate="key",
            validatecommand=self.validate_only_numbers,
        )
        self.n_questions_spbx.grid(row=0, column=1, pady=5)

        # Categories selector
        self._create_label(
            self.selection_screen, "Select category from the following list:", 1, 0
        )
        self.categories_lst = Listbox(self.selection_screen, height=5, width=37)
        for category in self.categories:
            self.categories_lst.insert(category["id"], category["name"])
        self.categories_lst.selection_set(0)
        self.categories_lst.grid(row=1, column=1, pady=5)

        # Difficulty selector
        self._create_label(
            self.selection_screen, "Choose the difficulty:", 2, 0, rowspan=3
        )
        self.radio_state = StringVar(value="easy")
        self._create_radiobutton("Easy", "easy", 2, 1)
        self._create_radiobutton("Medium", "medium", 3, 1)
        self._create_radiobutton("Hard", "hard", 4, 1)

        # Play Button
        play_button = Button(
            self.selection_screen, text="Play", command=self.start_game
        )
        play_button.grid(column=0, row=5, columnspan=2, sticky="EW")

    def setup_game_screen(self):
        """Sets up the main game screen for displaying trivia questions."""
        self.game_screen = Frame(self.window, padx=20, pady=10, bg=THEME_COLOR)

        # Back button
        self._create_button(
            self.game_screen, self.back_img, self.back_to_selection, 0, 0
        )

        # Score label
        self.score_lbl = self._create_label(
            self.game_screen,
            f"Score: {self._get_score_string()}",
            0,
            1,
        )

        # Trivia Canvas
        self.trivia_canvas = Canvas(self.game_screen, width=300, height=250, bg="white")
        self.trivia_text = self.trivia_canvas.create_text(
            150,
            125,
            text=self.current_trivia,
            font=(FONT_NAME, 20, "italic"),
            width=280,
            fill="black",
        )
        self.trivia_canvas.grid(row=1, column=0, columnspan=2, sticky="EW")

        # Choice Buttons
        # True
        self._create_button(
            self.game_screen,
            self.true_img,
            lambda: self._check_answer("True"),
            2,
            0,
        )
        # False
        self._create_button(
            self.game_screen,
            self.false_img,
            lambda: self._check_answer("False"),
            2,
            1,
        )

        # Configure grid weights for better responsiveness
        self.game_screen.grid_columnconfigure(0, weight=1)
        self.game_screen.grid_columnconfigure(1, weight=1)
        self.game_screen.grid_rowconfigure(1, weight=1)

    def start_game(self):
        """Starts the game if all inputs are valid."""
        if not self._validate_inputs():
            return  # Do not start the game if inputs are invalid

        # Hide selection screen and setup game screen
        self._set_question_bank()
        self.quiz = QuizBrain(self.question_bank)
        self.current_trivia = self._format_question(self.quiz.current_question())
        self.selection_screen.grid_forget()
        if not self.game_screen:
            self.setup_game_screen()
        self._reset_trivia_canvas()
        self.game_screen.grid(row=0, column=0)

    def back_to_selection(self):
        """Navigates back to the selection screen from the game screen."""
        # Hide game screen and show selection screen
        self._reset_game_screen()
        self.game_screen.grid_forget()
        self._show_selection_screen()

    def run(self):
        """Runs the main loop for the Tkinter window."""
        self._show_selection_screen()
        self.window.mainloop()


if __name__ == "__main__":
    quiz_app = QuizInterface()
    quiz_app.run()
