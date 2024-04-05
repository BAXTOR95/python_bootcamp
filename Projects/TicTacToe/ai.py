class TicTacToeAI:
    """AI logic for Tic Tac Toe using the minimax algorithm with alpha-beta pruning."""

    def __init__(self, board, ai_player):
        """
        Initializes the AI with the game board and player markers.

        Parameters:
            board (Board): The game board instance.
            ai_player (str): The marker for the AI player ('X' or 'O').
        """
        self.board = board
        self.ai_player = ai_player
        self.human_player = 'O' if ai_player == 'X' else 'X'

    def minimax(self, is_maximizing, alpha=float('-inf'), beta=float('inf')):
        """
        Finds the optimal move score using minimax algorithm with alpha-beta pruning.

        Parameters:
            is_maximizing (bool): True for maximizing player, False for minimizing.
            alpha (float): Best already explored option along path to the root for maximizer.
            beta (float): Best already explored option along path to the root for minimizer.

        Returns:
            int: The score of the best move.
        """
        # Check for a terminal state and return the corresponding score
        if self.board.check_win(self.ai_player):
            return 10
        elif self.board.check_win(self.human_player):
            return -10
        elif self.board.is_full():
            return 0

        if is_maximizing:
            max_eval = float('-inf')
            for row in range(3):
                for col in range(3):
                    if self.board.board[row][col] == ' ':  # Check if cell is empty
                        self.board.board[row][col] = self.ai_player  # Make a move
                        eval = self.minimax(
                            False, alpha, beta
                        )  # Recurse with the new board state
                        self.board.board[row][col] = ' '  # Undo the move
                        max_eval = max(max_eval, eval)
                        alpha = max(
                            alpha, eval
                        )  # Update alpha if a better max is found
                        if beta <= alpha:  # Cut-off condition
                            break
            return max_eval
        else:
            min_eval = float('inf')
            for row in range(3):
                for col in range(3):
                    if self.board.board[row][col] == ' ':
                        self.board.board[row][col] = self.human_player
                        eval = self.minimax(True, alpha, beta)
                        self.board.board[row][col] = ' '
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)  # Update beta if a better min is found
                        if beta <= alpha:  # Cut-off condition
                            break
            return min_eval

    def find_best_move(self):
        """
        Evaluates all possible moves on the board and returns the best move for the AI.

        Returns:
            tuple: Row and column indices for the best move.
        """
        best_score = float('-inf')
        best_move = None
        for row in range(3):
            for col in range(3):
                if self.board.board[row][col] == ' ':  # Check if the spot is available
                    self.board.board[row][col] = self.ai_player  # Test the move
                    score = self.minimax(False)  # Evaluate move
                    self.board.board[row][col] = ' '  # Undo the move
                    if (
                        score > best_score
                    ):  # Check if this move is better than the current best
                        best_score = score
                        best_move = (row, col)
        return best_move
