
# first message the operator receives, with instructions
def print_welcome_message():
    print("Welcome to the Python Calculator")
    print("Enter 'q' to quit")
    print("Enter 'o' for a list of operators")
    print("Enter 'c' to continue")
    entry = input("Waiting for input: ")
    return entry

# message the user receives if the input is invalid
def try_again_message():
    print("Invalid input")
    print("Please enter a valid instruction")
    print("To quit enter q")
    entry = input("Waiting for input: ")
    return entry


# prints the available operators
def print_operator_list():
    print("Binary operators: +, -, *, /, ^, %, $, &, @")
    print("Right unary operators: !, #")
    print("Left unary operators: ~")


# message the user receives when the program is closed
def print_goodbye_message():
    print("Goodbye!")


# message to continue after the operator list is printed or an unsuccessful equation is entered
def continue_message():
    print("To continue enter any key")
    print("To quit enter q")
    entry = input("Waiting for input: ")
    return entry


# message to continue after a successful equation is entered
def continue_after_solution_message():
    print("To enter another equation enter any key")
    print("To quit enter q")
    entry = input("Waiting for input: ")
    return entry


# message to get the equation from the user
def get_equation():
    equation = input("Enter equation: ")
    return equation
