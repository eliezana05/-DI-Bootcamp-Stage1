"""Exercise 1: favorite numbers."""

print("\nExercise 1: Favorite Numbers")
my_fav_numbers = {7, 12, 42}
my_fav_numbers.add(8)
my_fav_numbers.add(99)
# Sets are unordered, so remove the last added value explicitly.
my_fav_numbers.remove(99)
friend_fav_numbers = {3, 7, 21}
our_fav_numbers = my_fav_numbers.union(friend_fav_numbers)
print("My numbers:", my_fav_numbers)
print("Our numbers:", our_fav_numbers)
