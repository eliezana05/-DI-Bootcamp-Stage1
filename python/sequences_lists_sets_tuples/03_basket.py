"""Exercise 3: basket."""

print("\nExercise 3: List Manipulation")
basket = ["Banana", "Apples", "Oranges", "Blueberries"]
basket.remove("Banana")
basket.remove("Blueberries")
basket.append("Kiwi")
basket.insert(0, "Apples")
print("Number of Apples:", basket.count("Apples"))
basket.clear()
print("Final basket:", basket)
