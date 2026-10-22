"""Run with: python3 -m unittest discover -s python/day5/mini_projects -v"""

import contextlib
import io
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

import hangman
import tic_tac_toe as tic


FOLDER = Path(__file__).parent


def run_script(filename, answers):
    result = subprocess.run(
        [sys.executable, str(FOLDER / filename)],
        input="\n".join(str(answer) for answer in answers) + "\n",
        capture_output=True, text=True, timeout=5,
    )
    if result.returncode != 0:
        raise AssertionError(result.stderr)
    return result.stdout


class TicTacToeTests(unittest.TestCase):
    def test_new_board_has_independent_rows(self):
        board = tic.create_board()
        board[0][0] = "X"
        self.assertEqual(board[1][0], " ")
        self.assertEqual(board[2][0], " ")
        self.assertFalse(tic.check_win(board, "X"))
        self.assertFalse(tic.check_tie(board))

    def test_all_eight_winning_lines_for_both_players(self):
        lines = [
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
            [(0, 0), (1, 1), (2, 2)],
            [(0, 2), (1, 1), (2, 0)],
        ]
        for player in ["X", "O"]:
            for line in lines:
                with self.subTest(player=player, line=line):
                    board = tic.create_board()
                    for row, column in line:
                        board[row][column] = player
                    self.assertTrue(tic.check_win(board, player))
                    self.assertFalse(tic.check_win(board, "O" if player == "X" else "X"))

    def test_full_board_without_winner_is_tie(self):
        self.assertTrue(tic.check_tie([
            ["X", "O", "X"], ["X", "O", "O"], ["O", "X", "X"],
        ]))

    def test_full_winning_board_is_not_tie(self):
        self.assertFalse(tic.check_tie([
            ["X", "O", "X"], ["O", "X", "O"], ["O", "X", "X"],
        ]))

    def test_invalid_input_and_taken_cell_keep_same_turn(self):
        board = tic.create_board()
        board[0][0] = "X"
        answers = ["abc", "0", "1", "4", "1", "1", "1", "2", "3"]
        with patch("builtins.input", side_effect=answers), contextlib.redirect_stdout(io.StringIO()) as output:
            move = tic.player_input("O", board)
        self.assertEqual(move, (1, 2))
        self.assertEqual(board[1][2], " ")
        self.assertIn("whole numbers", output.getvalue())
        self.assertIn("between 1 and 3", output.getvalue())
        self.assertIn("already taken", output.getvalue())

    def test_complete_x_win_in_terminal(self):
        output = run_script("tic_tac_toe.py", [1, 1, 2, 1, 1, 2, 2, 2, 1, 3])
        self.assertIn("Player X wins!", output)
        self.assertNotIn("It's a tie!", output)

    def test_complete_o_win_in_terminal(self):
        output = run_script("tic_tac_toe.py", [1, 1, 2, 1, 1, 2, 2, 2, 3, 3, 2, 3])
        self.assertIn("Player O wins!", output)

    def test_complete_tie_in_terminal(self):
        output = run_script("tic_tac_toe.py", [1, 1, 1, 2, 1, 3, 2, 2, 2, 1, 2, 3, 3, 2, 3, 1, 3, 3])
        self.assertIn("It's a tie!", output)
        self.assertNotIn("wins!", output)

    def test_ninth_move_win_is_not_tie(self):
        output = run_script("tic_tac_toe.py", [1, 1, 1, 2, 1, 3, 2, 1, 2, 2, 2, 3, 3, 2, 3, 1, 3, 3])
        self.assertIn("Player X wins!", output)
        self.assertNotIn("It's a tie!", output)

    def test_input_end_stops_cleanly(self):
        self.assertIn("Game stopped", run_script("tic_tac_toe.py", []))


class HangmanTests(unittest.TestCase):
    def play_word(self, word, answers):
        with patch.object(hangman.random, "choice", return_value=word), patch("builtins.input", side_effect=answers), contextlib.redirect_stdout(io.StringIO()) as output:
            hangman.play()
        return output.getvalue()

    def test_initial_mask_and_spaces(self):
        self.assertEqual(hangman.hidden_word("credit card", []), "****** ****")

    def test_letter_revealed_in_every_position(self):
        self.assertEqual(hangman.hidden_word("correction", ["r", "o"]), "*orr****o*")
        self.assertEqual(hangman.hidden_word("credit card", ["c"]), "c***** c***")

    def test_invalid_and_repeated_letters_are_rejected(self):
        with patch("builtins.input", side_effect=["", "ab", "7", "é", "A", " Z "]), contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(hangman.get_guess(["a"]), "z")
        self.assertEqual(output.getvalue().count("Please enter one letter"), 4)
        self.assertIn("already guessed", output.getvalue())

    def test_win_with_uppercase_input(self):
        output = self.play_word("python", list("PYTHON"))
        self.assertIn("You win! The word was: python", output)
        self.assertNotIn("You lose", output)

    def test_phrase_win(self):
        output = self.play_word("credit card", list("credita"))
        self.assertIn("You win! The word was: credit card", output)

    def test_six_errors_end_game(self):
        output = self.play_word("python", list("abcdef"))
        self.assertEqual(output.count("That letter is not in the word."), 6)
        self.assertIn("Wrong guesses remaining: 0", output)
        self.assertIn("You lose! The word was: python", output)
        self.assertIn(hangman.STAGES[6], output)

    def test_duplicate_and_invalid_guesses_do_not_cost_lives(self):
        output = self.play_word("python", ["a", "a", "", "ab", "1"] + list("python"))
        self.assertEqual(output.count("That letter is not in the word."), 1)
        self.assertIn("Wrong guesses remaining: 5", output)
        self.assertIn("You win!", output)

    def test_real_random_game_in_terminal(self):
        # None of these six letters occurs in any word in the supplied list.
        output = run_script("hangman.py", list("zxjkqg"))
        self.assertIn("You lose!", output)
        self.assertEqual(output.count("That letter is not in the word."), 6)

    def test_input_end_stops_cleanly(self):
        self.assertIn("Game stopped", run_script("hangman.py", []))


if __name__ == "__main__":
    unittest.main()
