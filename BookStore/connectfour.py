import numpy as np
from typing import Tuple, Optional


class ConnectFour:
    def __init__(self, rows=6, cols=7):
        self.rows = rows
        self.cols = cols
        self.board = np.zeros((rows, cols), dtype=int)
        self.current_player = 1  # 1 for player, 2 for AI

    def is_valid_move(self, col: int) -> bool:
        return self.board[0][col] == 0

    def drop_piece(self, col: int, piece: int) -> bool:
        for row in range(self.rows - 1, -1, -1):
            if self.board[row][col] == 0:
                self.board[row][col] = piece
                return True
        return False

    def check_winner(self) -> Optional[int]:
        # Check horizontal
        for row in range(self.rows):
            for col in range(self.cols - 3):
                if (
                    self.board[row][col] != 0
                    and self.board[row][col]
                    == self.board[row][col + 1]
                    == self.board[row][col + 2]
                    == self.board[row][col + 3]
                ):
                    return self.board[row][col]

        # Check vertical
        for row in range(self.rows - 3):
            for col in range(self.cols):
                if (
                    self.board[row][col] != 0
                    and self.board[row][col]
                    == self.board[row + 1][col]
                    == self.board[row + 2][col]
                    == self.board[row + 3][col]
                ):
                    return self.board[row][col]

        # Check diagonal (positive slope)
        for row in range(self.rows - 3):
            for col in range(self.cols - 3):
                if (
                    self.board[row][col] != 0
                    and self.board[row][col]
                    == self.board[row + 1][col + 1]
                    == self.board[row + 2][col + 2]
                    == self.board[row + 3][col + 3]
                ):
                    return self.board[row][col]

        # Check diagonal (negative slope)
        for row in range(3, self.rows):
            for col in range(self.cols - 3):
                if (
                    self.board[row][col] != 0
                    and self.board[row][col]
                    == self.board[row - 1][col + 1]
                    == self.board[row - 2][col + 2]
                    == self.board[row - 3][col + 3]
                ):
                    return self.board[row][col]

        return None

    def is_board_full(self) -> bool:
        return all(self.board[0][col] != 0 for col in range(self.cols))

    def evaluate_window(self, window: list, piece: int) -> int:
        score = 0
        opp_piece = 1 if piece == 2 else 2

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(0) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(0) == 2:
            score += 2

        if window.count(opp_piece) == 3 and window.count(0) == 1:
            score -= 4

        return score

    def score_position(self, piece: int) -> int:
        score = 0

        # Score center column
        center_array = [int(i) for i in list(self.board[:, self.cols // 2])]
        center_count = center_array.count(piece)
        score += center_count * 3

        # Score horizontal
        for r in range(self.rows):
            row_array = [int(i) for i in list(self.board[r, :])]
            for c in range(self.cols - 3):
                window = row_array[c : c + 4]
                score += self.evaluate_window(window, piece)

        # Score vertical
        for c in range(self.cols):
            col_array = [int(i) for i in list(self.board[:, c])]
            for r in range(self.rows - 3):
                window = col_array[r : r + 4]
                score += self.evaluate_window(window, piece)

        # Score diagonal
        for r in range(self.rows - 3):
            for c in range(self.cols - 3):
                window = [self.board[r + i][c + i] for i in range(4)]
                score += self.evaluate_window(window, piece)

        for r in range(self.rows - 3):
            for c in range(self.cols - 3):
                window = [self.board[r + 3 - i][c + i] for i in range(4)]
                score += self.evaluate_window(window, piece)

        return score

    def get_valid_locations(self) -> list:
        valid_locations = []
        for col in range(self.cols):
            if self.is_valid_move(col):
                valid_locations.append(col)
        return valid_locations

    def minimax(
        self, depth: int, alpha: float, beta: float, maximizing_player: bool
    ) -> Tuple[int, int]:
        valid_locations = self.get_valid_locations()
        is_terminal = self.check_winner() is not None or self.is_board_full()

        if depth == 0 or is_terminal:
            if is_terminal:
                if self.check_winner() == 2:
                    return (None, 100000000000000)
                elif self.check_winner() == 1:
                    return (None, -100000000000000)
                else:  # Game is over, no more valid moves
                    return (None, 0)
            else:  # Depth is zero
                return (None, self.score_position(2))

        if maximizing_player:
            value = float("-inf")
            column = valid_locations[0]
            for col in valid_locations:
                row = next(
                    (r for r in range(self.rows - 1, -1, -1) if self.board[r][col] == 0)
                )
                temp_board = self.board.copy()
                self.drop_piece(col, 2)
                new_score = self.minimax(depth - 1, alpha, beta, False)[1]
                self.board = temp_board
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else:  # Minimizing player
            value = float("inf")
            column = valid_locations[0]
            for col in valid_locations:
                row = next(
                    (r for r in range(self.rows - 1, -1, -1) if self.board[r][col] == 0)
                )
                temp_board = self.board.copy()
                self.drop_piece(col, 1)
                new_score = self.minimax(depth - 1, alpha, beta, True)[1]
                self.board = temp_board
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value

    def ai_move(self) -> int:
        col, minimax_score = self.minimax(5, float("-inf"), float("inf"), True)
        return col

    def print_board(self):
        print("\n")
        for row in self.board:
            print("|", end=" ")
            for cell in row:
                if cell == 0:
                    print(".", end=" ")
                elif cell == 1:
                    print("X", end=" ")
                else:
                    print("O", end=" ")
            print("|")
        print("-" * (self.cols * 2 + 3))
        print("|", end=" ")
        for i in range(self.cols):
            print(i, end=" ")
        print("|\n")


def play_game():
    game = ConnectFour()
    game_over = False

    print("Welcome to Connect Four!")
    print("You are X, AI is O")
    print("Enter a column number (0-6) to make your move")

    while not game_over:
        game.print_board()

        # Player's turn
        if game.current_player == 1:
            while True:
                try:
                    col = int(input("Your move (0-6): "))
                    if 0 <= col < game.cols and game.is_valid_move(col):
                        break
                    else:
                        print("Invalid move. Try again.")
                except ValueError:
                    print("Please enter a number between 0 and 6.")

            game.drop_piece(col, 1)

        # AI's turn
        else:
            col = game.ai_move()
            game.drop_piece(col, 2)
            print(f"AI plays column {col}")

        # Check for winner
        winner = game.check_winner()
        if winner:
            game.print_board()
            if winner == 1:
                print("Congratulations! You win!")
            else:
                print("AI wins!")
            game_over = True

        # Check for draw
        elif game.is_board_full():
            game.print_board()
            print("It's a draw!")
            game_over = True

        # Switch players
        game.current_player = 3 - game.current_player


if __name__ == "__main__":
    play_game()
