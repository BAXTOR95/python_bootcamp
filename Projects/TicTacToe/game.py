from board import Board
from ai import TicTacToeAI


class Game:
    """
    Manages the Tic Tac Toe game play, including player interactions,
    switching turns, and determining the game outcome.
    """

    def __init__(self, starting_player='X'):
        """
        Initializes the game with a clean board and sets the starting player.
        """
        self.board = Board()
        self.current_player = starting_player  # Set the starting player
        self.ai_player = None  # AI player marker (None if not playing against AI)
        self.human_player = (
            'O' if starting_player == 'X' else 'X'
        )  # Human player marker

    def switch_player(self):
        """
        Switches the turn to the other player.
        """
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def choose_opponent(self):
        """
        Lets the user choose whether to play against another player or the AI.
        """
        choice = input(
            'Do you want to play against (1) Another Player or (2) the AI? Enter 1 or 2: '
        )
        if choice == '2':
            self.ai_player = 'O'  # AI plays with 'O'
            print('You chose to play against the AI. You are "X".')
        else:
            self.ai_player = None
            print('You chose to play against another player.')

    def get_player_move(self):
        """
        Gets the current player's move. If the move is invalid or the spot is taken,
        it prompts the player again.
        """
        while True:
            try:
                row, col = map(
                    int,
                    input(
                        f'Player {self.current_player}, enter your move as "row col": '
                    ).split(),
                )
                if self.board.update_board(row, col, self.current_player):
                    break
                else:
                    print('Spot taken, try again.')
            except (ValueError, IndexError):
                print('Invalid move, try again.')

    def make_ai_move(self):
        """
        Makes the AI player's move.
        """
        print(f'AI ({self.ai_player}) is making a move...')
        ai = TicTacToeAI(self.board, self.ai_player)
        row, col = ai.find_best_move()
        self.board.update_board(row, col, self.ai_player)
        print(f'AI placed {self.ai_player} on ({row}, {col}).')

    def play(self):
        """
        Starts and manages the game play until there's a winner or the board is full.
        """
        self.choose_opponent()  # Lets the user choose the opponent at the start
        if self.current_player == self.ai_player:
            self.make_ai_move()
            self.switch_player()

        while True:
            self.board.print_board()
            if self.current_player == self.ai_player:
                self.make_ai_move()
            else:
                self.get_player_move()

            if self.board.check_win(self.current_player):
                self.board.print_board()
                print(f'Player {self.current_player} wins!')
                break
            elif self.board.is_full():
                self.board.print_board()
                print('The game is a tie.')
                break

            self.switch_player()
