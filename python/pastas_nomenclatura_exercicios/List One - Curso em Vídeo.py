exercise_num = 0

"""Implement a functional code using Python that reads a person's name and displays a welcome message."""
# Function to read a person's name
def read_name():
    name = input('Enter you name: ')
    return name

# Function to display a welcome message
def display_welcome_message(name):
    print(f'Welcome, {name}, you little shit ass.')

#Higher-order function
def execute_program(read_funcion, display_function):
    name = read_funcion()
    display_function(name)

if __name__ == '__main__' and exercise_num == 1:
    execute_program(read_name, display_welcome_message)

"""Implement a functional code using Python that reads two numbers and displays the sum between them."""