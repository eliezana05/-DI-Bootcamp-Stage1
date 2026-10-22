"""Two-player Tic Tac Toe. Run: python3 tic_tac_toe.py

Course: section/56/chapter/278 (Mini-Project Day).
"""


def create_board():
    """Create three separate rows of empty cells."""
    return [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]


def display_board(board):
    """Display row and column numbers to help players choose a cell."""
    print("\n    1   2   3")
    for row_number, row in enumerate(board, start=1):
        print(f"{row_number}   " + " | ".join(row))
        if row_number < 3:
            print("   ---+---+---")
    print()


def player_input(player, board):
    """Read a valid empty cell; return its row and column indexes."""
    while True:
        try:
            row = int(input(f"Player {player}, choose a row (1-3): "))
            column = int(input("Choose a column (1-3): "))
        except ValueError:
            print("Please enter whole numbers from 1 to 3.")
            continue

        if not (1 <= row <= 3 and 1 <= column <= 3):
            print("The row and column must be between 1 and 3.")
            continue

        # Players count from 1, but Python indexes count from 0.
        row -= 1
        column -= 1
        if board[row][column] != " ":
            print("That cell is already taken. Choose another cell.")
            continue
        return row, column


def check_win(board, player):
    """Check all three rows, three columns, and two diagonals."""
    for index in range(3):
        if (board[index][0] == board[index][1] == board[index][2] == player):
            return True
        if (board[0][index] == board[1][index] == board[2][index] == player):
            return True
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True
    if board[0][2] == board[1][1] == board[2][0] == player:
        return True
    return False


def check_tie(board):
    """A full board is a tie only when neither player has won."""
    if check_win(board, "X") or check_win(board, "O"):
        return False
    for row in board:
        if " " in row:
            return False
    return True


def play():
    """Alternate turns until one player wins or the game is a tie."""
    board = create_board()
    player = "X"
    print("Welcome to Tic Tac Toe! X starts.")
    print("Choose a row and column from 1 to 3. Press Ctrl+C to stop.")
    display_board(board)

    while True:
        row, column = player_input(player, board)
        board[row][column] = player
        display_board(board)

        if check_win(board, player):
            print(f"Player {player} wins!")
            break
        if check_tie(board):
            print("It's a tie!")
            break

        if player == "X":
            player = "O"
        else:
            player = "X"


if __name__ == "__main__":
    try:
        play()
    except (KeyboardInterrupt, EOFError):
        print("\nGame stopped. Goodbye!")
