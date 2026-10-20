"""Exercise 2: tuple."""

print("\nExercise 2: Tuple")
numbers = (1, 2, 3)
try:
    # A tuple has no append method because it cannot grow in place.
    numbers.append(4)
except AttributeError:
    print("Un tuple est immuable : on ne peut pas modifier ses éléments.")
# Concatenation creates a new tuple and leaves the original unchanged.
extended_numbers = numbers + (4, 5)
print("Original:", numbers)
print("New tuple:", extended_numbers)
