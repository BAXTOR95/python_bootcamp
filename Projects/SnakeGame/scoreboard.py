from turtle import Turtle
import os


class Scoreboard(Turtle):
    """Scoreboard class"""

    STARTING_POSITION = (0, 265)
    ALIGNMENT = "center"
    FONT = ('Consolas', 24, 'bold')
    SAVE_PATH = "data.txt"

    def __init__(self) -> None:
        super().__init__(visible=False)
        self.score = 0
        self.high_score = self.get_high_score()
        self.penup()
        self.goto(self.STARTING_POSITION)
        self.color("white")
        self.show()

    def show(self):
        """Draws the scoreboard to screen"""
        self.write(
            f"Score: {self.score} High Score: {self.high_score}",
            align=self.ALIGNMENT,
            font=self.FONT,
        )

    def reset(self):
        """Resets the scoreboard"""
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_score()
        self.score = 0
        self.update_scoreboard()

    def update_scoreboard(self):
        """Refreshes the scoreboard"""
        self.clear()
        self.write(
            f"Score: {self.score} High Score: {self.high_score}",
            align=self.ALIGNMENT,
            font=self.FONT,
        )

    def get_high_score(self):
        if os.path.exists(self.SAVE_PATH):
            with open("data.txt", "r") as file:
                return int(file.read())
        else:
            return 0

    def save_score(self):
        with open("data.txt", "w") as file:
            file.write(str(self.score))

    # def game_over(self):
    #     """Draws game over message to screen
    #     """
    #     self.home()
    #     self.write("GAME OVER", align=self.ALIGNMENT, font=self.FONT)

    def increase_score(self):
        """Increases score at the scoreboard"""
        self.score += 1
        self.update_scoreboard()
