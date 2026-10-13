
# Exercise 1: Hello World
print("Hello world\n" * 4)

# Exercise 2: Some Math
print((99 ** 3) * 8)

# Exercise 3: What is the output?

print(5 < 3)               # False
print(3 == 3)              # True
print(3 == "3")            # False
print("Hello" == "hello")  # False

# Exercise 4: Your Computer Brand

computer_brand = "Apple"

print(f"I have a {computer_brand} computer.")

# Exercise 5: Your Information

name = "Elie"
age = 21
shoe_size = 44

info = f"My name is {name}, I am {age} years old and my shoe size is {shoe_size}."

print(info)

# Exercise 6: A & B

a = 10
b = 5

if a > b:
    print("Hello World")

# Exercise 7: Odd or Even

number = int(input("Enter a number: "))

if number % 2 == 0:
    print("Even number")
else:
    print("Odd number")

# Exercise 8: What's Your Name?

my_name = "Elie"

user_name = input("What is your name? ")

if user_name.lower() == my_name.lower():
    print("Wow! We have the same name! Are you my twin?")
else:
    print("Nice name! But mine is cooler!")

# Exercise 9: Roller Coaster

height = float(input("Enter your height in cm: "))

if height > 145:
    print("You are tall enough to ride!")
else:
    print("Sorry, you need to grow some more to ride!")
