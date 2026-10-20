"""Exercise 7: favorite fruits."""

print("\nExercise 7: Favorite Fruits")
favorite_fruits = input("Tes fruits préférés, séparés par des espaces : ").lower().split()
fruit = input("Choisis un fruit : ").strip().lower()
if fruit in favorite_fruits:
    print("You chose one of your favorite fruits! Enjoy!")
else:
    print("You chose a new fruit. I hope you enjoy it!")
