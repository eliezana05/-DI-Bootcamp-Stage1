"""Exercise 6: name validation."""

print("\nExercise 6: While Loop")
while True:
    name = input("Entre ton prénom (au moins 3 lettres) : ").strip()
    if not name.isdigit() and name.isalpha() and len(name) >= 3:
        print("thank you")
        break
    print("Prénom incorrect : utilise au moins 3 lettres, sans chiffres.")
