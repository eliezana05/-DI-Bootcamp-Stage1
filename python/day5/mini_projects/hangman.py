"""Guess the word or phrase before making six wrong guesses.

Run: python3 hangman.py
Course: section/56/chapter/279 (Mini-Project Day).
"""

import random


WORDSLIST = [
    "correction", "childish", "beach", "python", "assertive",
    "interference", "complete", "share", "credit card", "rush", "south",
]

# Each new stage adds exactly one body part.
STAGES = [
    " +---+\n |   |\n     |\n     |\n     |\n=======",
    " +---+\n |   |\n O   |\n     |\n     |\n=======",
    " +---+\n |   |\n O   |\n |   |\n     |\n=======",
    " +---+\n |   |\n O   |\n/|   |\n     |\n=======",
    " +---+\n |   |\n O   |\n/|\\  |\n     |\n=======",
    " +---+\n |   |\n O   |\n/|\\  |\n/    |\n=======",
    " +---+\n |   |\n O   |\n/|\\  |\n/ \\  |\n=======",
]


def hidden_word(word, guessed_letters):
    """Reveal every matching letter and keep spaces between words."""
    result = ""
    for letter in word:
        if letter == " " or letter in guessed_letters:
            result += letter
        else:
            result += "*"
    return result


def get_guess(guessed_letters):
    """Reject empty input, non-letters, and repeated guesses."""
    while True:
        guess = input("Guess one letter (a-z): ").strip().lower()
        if len(guess) != 1 or guess not in "abcdefghijklmnopqrstuvwxyz":
            print("Please enter one letter from a to z.")
            continue
        if guess in guessed_letters:
            print("You already guessed that letter. Try a different one.")
            continue
        return guess


def display_game(word, guessed_letters, mistakes):
    """Show the gallows, hidden word, guesses, and remaining chances."""
    print("\n" + STAGES[mistakes])
    print("Word:", hidden_word(word, guessed_letters))
    print("Guessed letters:", ", ".join(guessed_letters) or "none")
    print("Wrong guesses remaining:", 6 - mistakes)


def play():
    """Choose a random word and play until a win or six mistakes."""
    word = random.choice(WORDSLIST)
    guessed_letters = []
    mistakes = 0
    print("Welcome to Hangman! You can make six wrong guesses.")
    print("Spaces are shown automatically. Press Ctrl+C to stop.")
    display_game(word, guessed_letters, mistakes)

    while mistakes < 6:
        guess = get_guess(guessed_letters)
        guessed_letters.append(guess)
        if guess in word:
            print("Good guess!")
        else:
            mistakes += 1
            print("That letter is not in the word.")

        display_game(word, guessed_letters, mistakes)
        if "*" not in hidden_word(word, guessed_letters):
            print(f"You win! The word was: {word}")
            return

    print(f"You lose! The word was: {word}")


if __name__ == "__main__":
    try:
        play()
    except (KeyboardInterrupt, EOFError):
        print("\nGame stopped. Goodbye!")
