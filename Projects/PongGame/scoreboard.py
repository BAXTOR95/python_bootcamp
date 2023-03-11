from turtle import Turtle


class Scoreboard(Turtle):
    """Scoreboard class
    """
    def __init__(self) -> None:
        super().__init__(visible=False)
        self.color("white")
        self.penup()
        self.p1_score = 0
        self.p2_score = 0
        self.update_scoreboard()

    def update_scoreboard(self):
        """Draws scoreboard to screen
        """
        self.clear()
        self.goto(-100, 200)
        self.write(self.p1_score, align="center",
                   font=("Consolas", 70, "normal"))
        self.goto(100, 200)
        self.write(self.p2_score, align="center",
                   font=("Consolas", 70, "normal"))

    def p1_point(self):
        """Increases P1 score
        """
        self.p1_score += 1
        self.update_scoreboard()

    def p2_point(self):
        """Increases P2 score
        """
        self.p2_score += 1
        self.update_scoreboard()
