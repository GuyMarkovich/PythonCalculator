
def print_welcome_message():
    print("Welcome to the Python Calculator")
    print("Enter 'q' to quit")
    print("Enter 'o' for a list of operators")
    print("Enter 'c' to continue")
    entry = input("Waiting for input: ")
    return entry


def try_again_message():
    print("Invalid input")
    print("Please enter a valid instruction")
    print("To quit enter q")
    entry = input("Waiting for input: ")
    return entry


def print_operator_list():
    print("Binary operators: +, -, *, /, ^, %, $, &, @")
    print("Right unary operators: !, #")
    print("Left unary operators: ~")


def print_goodbye_message():
    print("Goodbye!")


def continue_message():
    print("To continue enter c")
    print("To quit enter q")
    entry = input("Waiting for input: ")
    return entry


def continue_after_solution_message():
    print("To enter another equation press enter")
    print("To quit enter q")
    entry = input("Waiting for input: ")
    return entry


def get_equation():
    equation = input("Enter equation: ")
    return equation
