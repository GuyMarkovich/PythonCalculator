from user_interface import *
from input_handler import *


def main():
    user_input: str = ''
    try:
        user_input = print_welcome_message()
    except EOFError as e:
        print("EOF is not a valid input, please relaunch the program")
        exit(0)

    while user_input != 'q' and user_input != 'o' and user_input != 'c':
        user_input = try_again_message()
    if user_input == 'o':
        print_operator_list()
        user_input = continue_message()
    elif user_input == 'c':
        pass
    elif user_input == 'q':
        print_goodbye_message()
        exit()

    while user_input != 'q':
        equation = get_equation()
        result = calculate_equation(equation)
        if result == 'Error':
            user_input = continue_message()
        else:
            print(result)
            user_input = continue_after_solution_message()

    print_goodbye_message()


if __name__ == '__main__':
    main()
