"""Exercise 5: for loop."""

print("\nExercise 5: For Loop")
for number in range(1, 21):
    print(number)
print("Numbers at even indices (Python indices start at 0):")
for index, number in enumerate(range(1, 21)):
    if index % 2 == 0:
        print(number)
