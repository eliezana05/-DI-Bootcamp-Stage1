"""Exercise 8: pizza toppings."""

print("\nExercise 8: Pizza Toppings")
toppings = []
while True:
    topping = input("Garniture de pizza (quit pour terminer) : ").strip()
    if topping.lower() == "quit":
        break
    if not topping:
        print("Entre une garniture.")
        continue
    toppings.append(topping)
    print(f"Adding {topping} to your pizza.")
total_price = 10 + len(toppings) * 2.50
print("Toppings:", toppings)
print(f"Total pizza cost: ${total_price:.2f}")
