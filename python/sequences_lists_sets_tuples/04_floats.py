"""Exercise 4: floats."""

print("\nExercise 4: Floats")
print("Un int est un entier ; un float représente un nombre à virgule.")
print("Exemples : 2 est un int, 2.0 et 1.5 sont des floats.")
# Divide by two; use integer division for whole numbers.
sequence = []
for number in range(3, 11):
    if number % 2 == 0:
        sequence.append(number // 2)
    else:
        sequence.append(number / 2)
print(sequence)
