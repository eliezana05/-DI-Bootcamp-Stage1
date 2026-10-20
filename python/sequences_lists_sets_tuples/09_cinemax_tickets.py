"""Exercise 9: cinemax tickets."""

def read_age(prompt):
    """Read a non-negative integer age, or 'quit' to stop."""
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
# Loop over a copy to remove people without skipping anyone.
for person, age in attendees.copy():
    if not 16 <= age <= 21:
        attendees.remove((person, age))
print("Final attendees:", attendees)
