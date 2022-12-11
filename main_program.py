from user_interface import *

user_input = print_welcome_message()
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
    print(equation)
    user_input = continue_after_solution_message()

print_goodbye_message()
