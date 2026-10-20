"""Day 3 - Exercises XP: dictionaries, including both bonuses.

Run: python3 python/day3/exercises_xp/submission.py
Source: https://octopus.developers.institute/courses/collection/254/course/1067/section/54/chapter/246
"""


def ticket_price(age):
    """Return the ticket price for a non-negative age."""
    if age < 3:
        return 0
    elif age <= 12:
        return 10
    else:
        return 15


def print_family_cost(family):
    """Print each person's ticket price and the family total."""
    total_cost = 0
    for name, age in family.items():
        price = ticket_price(age)
        print(f"{name}: ${price}")
        total_cost += price
    print(f"Total ticket cost: ${total_cost}")


def main():
    # Exercise 1: Match each key to the value at the same position.
    print("Exercise 1 - Converting Lists into Dictionaries")
    keys = ["Ten", "Twenty", "Thirty"]
    values = [10, 20, 30]
    numbers = dict(zip(keys, values))
    print(numbers)

    # Exercise 2: Calculate the price for each member of the given family.
    print("\nExercise 2 - Cinemax #2")
    family = {"rick": 43, "beth": 13, "morty": 5, "summer": 8}
    print_family_cost(family)  # Expected total: $50.

    # Bonus: Build a new family dictionary from the user's answers.
    print("\nBonus - Enter your family members")
    user_family = {}
    while True:
        name = input("Family member's name (quit to finish): ").strip()
        if name.lower() == "quit":
            break
        if not name:
            print("Please enter a name.")
            continue
        if name in user_family:
            print("This name is already used. Enter a different name.")
            continue

        while True:
            answer = input(f"Age of {name}: ").strip()
            try:
                age = int(answer)
                if age >= 0:
                    break
            except ValueError:
                pass
            print("Please enter a whole number greater than or equal to 0.")
        user_family[name] = age

    print("Your family:", user_family)
    print_family_cost(user_family)

    # Exercise 3: Store Zara's information in a nested dictionary.
    print("\nExercise 3 - Zara")
    brand = {
        "name": "Zara",
        "creation_date": 1975,
        "creator_name": "Amancio Ortega Gaona",
        "type_of_clothes": ["men", "women", "children", "home"],
        "international_competitors": ["Gap", "H&M", "Benetton"],
        "number_stores": 7000,
        "major_color": {
            "France": "blue",
            "Spain": "red",
            "US": ["pink", "green"],
        },
    }
    brand["number_stores"] = 2
    print("Number of stores:", brand["number_stores"])
    print("Zara offers clothes for", ", ".join(brand["type_of_clothes"][:3]),
          "and products for the", brand["type_of_clothes"][3] + ".")
    brand["country_creation"] = "Spain"

    if "international_competitors" in brand:
        brand["international_competitors"].append("Desigual")

    brand.pop("creation_date")
    print("Last competitor:", brand["international_competitors"][-1])
    print("Major colors in the US:", brand["major_color"]["US"])
    print("Number of keys:", len(brand))  # Expected: 7.
    print("All keys:", list(brand.keys()))
    print("Brand before the bonus:", brand)

    # Bonus: These are example values because the task does not specify them.
    # update adds creation_date back and replaces the number_stores value.
    more_on_zara = {"creation_date": 1975, "number_stores": 10000}
    brand.update(more_on_zara)
    print("Merged brand:", brand)

    # Exercise 4: Build three dictionaries using ordinary for loops.
    print("\nExercise 4 - Disney Characters")
    users = ["Mickey", "Minnie", "Donald", "Ariel", "Pluto"]

    disney_users_a = {}
    for index, character in enumerate(users):
        disney_users_a[character] = index
    print("Characters to indices:", disney_users_a)

    disney_users_b = {}
    for index, character in enumerate(users):
        disney_users_b[index] = character
    print("Indices to characters:", disney_users_b)

    disney_users_c = {}
    for index, character in enumerate(sorted(users)):
        disney_users_c[character] = index
    print("Alphabetical characters to indices:", disney_users_c)


if __name__ == "__main__":
    main()
