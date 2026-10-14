"""Exercices Python : listes, sets, tuples et boucles.

Exécution : python3 exercises.py
Les nombres préférés sont des exemples à personnaliser.
"""


def read_age(prompt):
    """Demande un âge entier positif ou nul, ou 'quit' pour terminer."""
    while True:
        answer = input(prompt).strip()
        if answer.lower() == "quit":
            return None
        try:
            age = int(answer)
            if age >= 0:
                return age
        except ValueError:
            pass
        print("Entre un âge entier positif ou nul, ou quit.")


def main():
    print("\nExercise 1: Favorite Numbers")
    my_fav_numbers = {7, 12, 42}
    my_fav_numbers.add(8)
    my_fav_numbers.add(99)
    # Un set n'a pas d'ordre : on retire explicitement le dernier ajout.
    my_fav_numbers.remove(99)
    friend_fav_numbers = {3, 7, 21}
    our_fav_numbers = my_fav_numbers.union(friend_fav_numbers)
    print("My numbers:", my_fav_numbers)
    print("Our numbers:", our_fav_numbers)

    print("\nExercise 2: Tuple")
    numbers = (1, 2, 3)
    try:
        numbers[0] = 4
    except TypeError:
        print("Un tuple est immuable : on ne peut pas modifier ses éléments.")
    # La concaténation crée un nouveau tuple sans modifier l'original.
    extended_numbers = numbers + (4, 5)
    print("Original:", numbers)
    print("New tuple:", extended_numbers)

    print("\nExercise 3: List Manipulation")
    basket = ["Banana", "Apples", "Oranges", "Blueberries"]
    basket.remove("Banana")
    basket.remove("Blueberries")
    basket.append("Kiwi")
    basket.insert(0, "Apples")
    print("Number of Apples:", basket.count("Apples"))
    basket.clear()
    print("Final basket:", basket)

    print("\nExercise 4: Floats")
    print("Un int est un entier ; un float représente un nombre à virgule.")
    print("Exemples : 2 est un int, 2.0 et 1.5 sont des floats.")
    sequence = []
    for number in range(3, 11):
        if number % 2 == 0:
            sequence.append(number // 2)
        else:
            sequence.append(number / 2)
    print(sequence)

    print("\nExercise 5: For Loop")
    for number in range(1, 21):
        print(number)
    print("Numbers at even indices (Python indices start at 0):")
    for index, number in enumerate(range(1, 21)):
        if index % 2 == 0:
            print(number)

    print("\nExercise 6: While Loop")
    while True:
        name = input("Entre ton prénom (au moins 3 lettres) : ").strip()
        if not name.isdigit() and name.isalpha() and len(name) >= 3:
            print("thank you")
            break
        print("Prénom incorrect : utilise au moins 3 lettres, sans chiffres.")

    print("\nExercise 7: Favorite Fruits")
    favorite_fruits = input("Tes fruits préférés, séparés par des espaces : ").lower().split()
    fruit = input("Choisis un fruit : ").strip().lower()
    if fruit in favorite_fruits:
        print("You chose one of your favorite fruits! Enjoy!")
    else:
        print("You chose a new fruit. I hope you enjoy it!")

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

    print("\nExercise 9: Cinemax Tickets")
    family_ages = []
    while True:
        age = read_age("Âge d'un membre de la famille (quit pour terminer) : ")
        if age is None:
            break
        family_ages.append(age)
    total_cost = 0
    for age in family_ages:
        if age < 3:
            total_cost += 0
        elif age <= 12:
            total_cost += 10
        else:
            total_cost += 15
    print(f"Total ticket cost: ${total_cost:.2f}")

    print("\nBonus: Restricted Movie (16–21 inclusive)")
    attendees = []
    while True:
        person = input("Nom du participant (quit pour terminer) : ").strip()
        if person.lower() == "quit":
            break
        if not person:
            print("Entre un nom.")
            continue
        age = read_age(f"Âge de {person} (quit pour terminer) : ")
        if age is None:
            break
        attendees.append((person, age))
    # Parcourir une copie permet de retirer des éléments sans en sauter.
    for person, age in attendees.copy():
        if not 16 <= age <= 21:
            attendees.remove((person, age))
    print("Final attendees:", attendees)


if __name__ == "__main__":
    main()
