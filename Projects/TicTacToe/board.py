class Board:
    """Represents a Tic Tac Toe board."""

    def __init__(self):
        """Initializes an empty Tic Tac Toe board."""
        self.board = [[' ' for _ in range(3)] for _ in range(3)]

    def print_board(self):
        """Prints the current state of the board with improved spacing for a square appearance."""
        for i, row in enumerate(self.board):
            # Adding extra space for each cell and piping
            print(' ' + ' | '.join(row) + ' ')

            # Only print the row divider if it's not the last row
            if i < len(self.board) - 1:
                # Adjusting divider length to align with the cell spacing
                print('---+---+---')

    def update_board(self, row, col, player):
        """
        Attempts to place the player's mark on the specified position.

        Parameters:
            row (int): The row to update (0-based).
            col (int): The column to update (0-based).
            player (str): The player's mark ('X' or 'O').

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        if 0 <= row < 3 and 0 <= col < 3 and self.board[row][col] == ' ':
            self.board[row][col] = player
            return True
        return False

    def is_full(self):
        """Checks if the board is full."""
        return all(all(cell != ' ' for cell in row) for row in self.board)

    def check_win(self, player):
        """
        Checks if the specified player has won the game.

        Parameters:
            player (str): The player's mark to check for a win ('X' or 'O').

        Returns:
            bool: True if the player has won, False otherwise.
        """
        win_conditions = [
            [self.board[0][0], self.board[0][1], self.board[0][2]],
            [self.board[1][0], self.board[1][1], self.board[1][2]],
            [self.board[2][0], self.board[2][1], self.board[2][2]],
            [self.board[0][0], self.board[1][0], self.board[2][0]],
            [self.board[0][1], self.board[1][1], self.board[2][1]],
            [self.board[0][2], self.board[1][2], self.board[2][2]],
            [self.board[0][0], self.board[1][1], self.board[2][2]],
            [self.board[2][0], self.board[1][1], self.board[0][2]],
        ]
        return any(
            all(cell == player for cell in condition) for condition in win_conditions
        )
