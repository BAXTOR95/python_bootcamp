from turtle import Turtle


class Scoreboard(Turtle):
    """Scoreboard class
    """
    STARTING_POSITION = (0, 265)
    ALIGNMENT = "center"
    FONT = ('Consolas', 24, 'bold')

    def __init__(self) -> None:
        super().__init__(visible=False)
        self.score = 0
        self.penup()
        self.goto(self.STARTING_POSITION)
        self.color("white")
        self.show()

    def show(self):
        """Draws the scoreboard to screen
        """
        self.write(f"Score: {self.score}",
                   align=self.ALIGNMENT, font=self.FONT)

    def game_over(self):
        """Draws game over message to screen
        """
        self.home()
        self.write("GAME OVER", align=self.ALIGNMENT, font=self.FONT)

    def increase_score(self):
        """Increases score at the scoreboard
        """
        self.score += 1
        self.clear()
        self.show()
