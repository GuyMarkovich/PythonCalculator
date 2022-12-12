from globals import *
from classes import *


def append_operand(op_str, curr_equation, cnt_holder):
    """Function to append the accumulated operand string to the equation list as one operand"""
    if op_str.get_op_str() != '':
        temp_lst = [op_str.get_op_str(), 'operand', 0]
        curr_equation.equation.append(temp_lst)
        # reset operand string
        op_str.empty_op_str()
        # reset tilde count when operand is appended
        cnt_holder.tilde_reset()


def append_minus(raw_input, index, curr_equation, cnt_holder, op_str):
    """function for appending minus sighs, handles cases with multiple minus signs and their placement"""
    # in case of multiple minus signs:
    if cnt_holder.get_minus_cnt() > 1:
        # if list is previously empty, the minus sign is a left unary operator
        if len(curr_equation.equation) == 0:
            if cnt_holder.get_minus_cnt() % 2 == 1:
                # special case for unary minuses at the beginning of the equation when the first non
                # minus char is a parenthesis, we can append a tilde instead of a minus
                if raw_input[index] == '(':
                    temp_lst = ['~', 'operator', opDict['~'] + cnt_holder.get_parentheses_multiplier()]
                    curr_equation.equation.append(temp_lst)
                # in any other case a minus in the beginning of the equation will be appended to the operand string
                else:
                    op_str.add_to_beginning('-')
                cnt_holder.reset_minus_cnt()
            else:  # if even number of minus signs, no need to append anything to the operand so just reset the count
                cnt_holder.reset_minus_cnt()
        # if last character on list is a binary operator, left unary operator or an open parenthesis the minus is a
        # left unary operator
        elif curr_equation.equation[len(curr_equation.equation) - 1][0] in binOps \
                or curr_equation.equation[len(curr_equation.equation) - 1][0] in leftUnOps \
                or curr_equation.equation[len(curr_equation.equation) - 1][0] == '(':
            if cnt_holder.get_minus_cnt() % 2 == 1:
                op_str.add_to_beginning('-')
                cnt_holder.reset_minus_cnt()
            else:
                cnt_holder.reset_minus_cnt()
        # else: one minus will be added to the operand string and the rest will be counted as a binary operator
        else:
            if (cnt_holder.get_minus_cnt() - 1) % 2 == 1:
                temp_lst = ['-', 'operator', opDict['-'] + cnt_holder.get_parentheses_multiplier()]
                curr_equation.equation.append(temp_lst)
                cnt_holder.reset_minus_cnt()
                op_str.add_to_beginning('-')
                cnt_holder.reset_minus_cnt()
            else:
                temp_lst = ['+', 'operator', opDict['+'] + cnt_holder.get_parentheses_multiplier()]
                curr_equation.equation.append(temp_lst)
                cnt_holder.reset_minus_cnt()
                op_str.add_to_beginning('-')
                cnt_holder.reset_minus_cnt()
    # if only one minus sign, check if it is a left unary operator
    elif cnt_holder.get_minus_cnt() == 1:
        # if list is currently empty, the previous char is a binary operator, or the previous char is a left unary
        # operator the minus is a left unary operator
        if curr_equation.equation[len(curr_equation.equation) - 1][0] in binOps \
                or curr_equation.equation[len(curr_equation.equation) - 1][0] in leftUnOps \
                or len(curr_equation.equation) == 0:
            op_str.add_to_beginning('-')
            cnt_holder.reset_minus_cnt()
        else:
            temp_lst = ['-', 'operator', opDict['-'] + cnt_holder.get_parentheses_multiplier()]
            curr_equation.equation.append(temp_lst)
            cnt_holder.reset_minus_cnt()


def check_binOps(index, raw_input, curr_equation, cnt_holder, op_str):
    # minus is the only binary operator that can be the first character since it is also a left unary operator
    if index == 0 and raw_input[index] != '-':
        raise SyntaxError(
            f"Invalid character: {raw_input[index]} in equation at index {index}, binary operator cannot be first "
            f"character")
    elif index == len(raw_input) - 1:
        raise SyntaxError(
            f"Invalid character: {raw_input[index]} in equation at index {index}, binary operator cannot be last "
            f"character")
    # if the previous character is not an operand, a closed parenthesis, or a right unary operator, throw a syntax error
    elif raw_input[index] != '-' and (raw_input[index - 1] not in operands and raw_input[index - 1] != ')'
                                      and raw_input[index - 1] not in rightUnOps and raw_input[index - 1] != '-'):
        raise SyntaxError(
            f"Invalid character: {raw_input[index]} in equation at index {index}, binary operator must be "
            f"preceded by a number, closed parenthesis, minus, or another right unary operator")
    # if the next character is not an operand, an open parenthesis, or a left unary operator, or a minus throw a
    # syntax error
    elif raw_input[index + 1] not in operands and raw_input[index + 1] != '(' \
            and raw_input[index + 1] not in leftUnOps and raw_input[index + 1] != '-':
        raise SyntaxError(
            f"Invalid character: {raw_input[index]} in equation at index {index}, binary operator must be "
            f"followed by a number, minus, open parenthesis, or another left unary operator")
    # if passed all checks, append to curr_equation
    else:
        # keep count of how many minus signs have been seen
        if raw_input[index] == '-':
            cnt_holder.inc_minus_cnt()
        # decimal should be appended to the operand string and not as a binary operator
        elif raw_input[index] == '.':
            op_str.add_to_op_str(raw_input[index])
        else:
            temp_lst = [raw_input[index], 'operator',
                        opDict[raw_input[index]] + cnt_holder.get_parentheses_multiplier()]
            curr_equation.equation.append(temp_lst)


def check_leftUnOps(index, raw_input, curr_equation, cnt_holder, op_str):
    if index == len(raw_input) - 1:
        raise SyntaxError(
            f"Invalid character: {raw_input[index]} in equation at index {index}, left unary operator cannot be "
            f"last character")
    # if the next character is not an operand, an open parenthesis, or a left unary operator, or a minus throw a
    # syntax error
    elif raw_input[index + 1] not in operands and raw_input[index + 1] != '(' \
            and raw_input[index + 1] not in leftUnOps and raw_input[index + 1] != '-':
        raise SyntaxError(f"Invalid character: {raw_input[index]} in equation at index {index}, left unary operator "
                          f"must be followed by a number, minus, open parenthesis, or another left unary operator")
    # if the previous character is not a binary operator or an open parenthesis, throw a syntax error
    elif index != 0 and raw_input[index - 1] not in binOps and raw_input[index - 1] != '(' and raw_input[index - 1] not \
            in leftUnOps:
        raise SyntaxError(f"Invalid character: {raw_input[index]} in equation at index {index}, left unary operator "
                          f"must be preceded by a binary operator, another left unary operator or an open parenthesis")
    # if passed all checks, append to curr_equation
    else:
        # if operator is a tilde (~), increment tilde count
        if raw_input[index] == '~':
            cnt_holder.inc_tilde_cnt()
        # if tilde count is more than 1, throw a syntax error
        if cnt_holder.get_tilde_cnt() > 1:
            raise SyntaxError(f"Invalid character: {raw_input[index]} in equation at index {index}, tilde (~) "
                              f"cannot be used more than once on one operand")

        # since a left unary operator can appear after a minus we need to append any previously counted minus signs
        append_minus(raw_input, index, curr_equation, cnt_holder, op_str)

        temp_lst = [raw_input[index], 'operator', opDict[raw_input[index]] + cnt_holder.parentheses_multiplier]
        curr_equation.equation.append(temp_lst)


def check_rightUnOps(index, raw_input, curr_equation, cnt_holder):
    if index == 0:
        raise SyntaxError(
            f"Invalid character: {raw_input[index]} in equation at index {index}, right unary operator cannot be "
            f"first character")
    # if the previous character is not an operator or an open parenthesis, throw a syntax error
    elif raw_input[index - 1] not in operands and raw_input[index - 1] != ')' \
            and raw_input[index - 1] not in rightUnOps:
        raise SyntaxError(f"Invalid character: {raw_input[index]} in equation at index {index}, right unary operator "
                          f"must follow an operand or a closed parenthesis")
    # if next character is not a binary operator, or a right unary operator, or a closed parenthesis, throw a syntax
    # error
    elif index != len(raw_input) - 1 and raw_input[index + 1] not in binOps and raw_input[index + 1] not in rightUnOps \
            and raw_input[index + 1] != ')':
        raise SyntaxError(f"Invalid character: {raw_input[index]} in equation at index {index}, right unary operator "
                          f"must be followed by a binary operator, another right unary operator, or a closed "
                          f"parenthesis")
    # if passed all checks, append to curr_equation
    else:
        temp_lst = [raw_input[index], 'operator', opDict[raw_input[index]] + cnt_holder.get_parentheses_multiplier()]
        curr_equation.equation.append(temp_lst)


def check_allOps(index, raw_input, curr_equation, cnt_holder, op_str):
    """divide all operators into their respective categories"""
    if raw_input[index] in binOps:
        check_binOps(index, raw_input, curr_equation, cnt_holder, op_str)
        return
    elif raw_input[index] in rightUnOps:
        check_rightUnOps(index, raw_input, curr_equation, cnt_holder)
        return
    elif raw_input[index] in leftUnOps:
        check_leftUnOps(index, raw_input, curr_equation, cnt_holder, op_str)
        return


# check if input is valid
# if not, return error message
# else, return new equation without unnecessary characters
def check_input(raw_input, curr_equation, op_str, cnt_holder: CounterHolder):
    """check if user input is valid"""
    # remove all spaces and tabs
    raw_input = raw_input.replace(' ', '')
    raw_input = raw_input.replace('\t', '')

    index = 0
    for i in raw_input:
        if i in operands:
            # append any previously counted minus signs
            append_minus(raw_input, index, curr_equation, cnt_holder, op_str)
            # add operand to the string
            op_str.add_to_op_str(raw_input[index])
            index += 1
        elif i in allOps:
            # if operator is a decimal point no need to get rid of the stored operand string
            # before adding it to the number
            if i != '.':
                append_operand(op_str, curr_equation, cnt_holder)

            check_allOps(index, raw_input, curr_equation, cnt_holder, op_str)
            index += 1
        elif i == '(':
            append_minus(raw_input, index, curr_equation, cnt_holder, op_str)
            # if the previous character is a number or a right unary operator throw a syntax error
            if index != 0 and (raw_input[index - 1] in operands or raw_input[index - 1] in rightUnOps):
                raise SyntaxError(f"Invalid character: {raw_input[index]} in equation at index {index}, open "
                                  f"parenthesis cannot follow a number or a right unary operator")

            cnt_holder.tilde_reset()  # reset tilde count when open parenthesis is appended
            cnt_holder.parentheses_multiplier += 10
            temp_lst = [raw_input[index], 'operator',
                        opDict[raw_input[index]] + cnt_holder.get_parentheses_multiplier()]
            curr_equation.equation.append(temp_lst)
            index += 1
        elif i == ')':

            append_operand(op_str, curr_equation, cnt_holder)

            temp_lst = [raw_input[index], 'operator',
                        opDict[raw_input[index]] + cnt_holder.get_parentheses_multiplier()]
            cnt_holder.parentheses_multiplier -= 10
            curr_equation.equation.append(temp_lst)
            index += 1
        else:
            raise SyntaxError(f"Invalid character: {raw_input[index]} in equation at index {index}")
    # append last operand to the new equation if exists
    if index == len(raw_input):
        append_operand(op_str, curr_equation, cnt_holder)
    if cnt_holder.get_parentheses_multiplier() != 0:
        raise SyntaxError("Parentheses unbalanced")

    return curr_equation


def main():
    cnt_holder = CounterHolder()

    op_str = OpString('')  # string to hold the operators, temporary variable to be used in the check_input function
    curr_equation = Equation()  # equation object to hold the equation
    # receive equation from user:
    try:
        raw_input = input("Input your equation here: ")
    except EOFError:
        print("EOF entered, please retry with a valid equation")
        exit(1)
    try:
        curr_equation = check_input(raw_input, curr_equation, op_str, cnt_holder)
        print(raw_input)
        print(curr_equation.equation)
    except SyntaxError as e:
        print(e)
        print("Your equation: " + raw_input)
        exit(1)


if __name__ == '__main__':
    main()

# things to be added:
# change input lst to an object of type Equation
# the Object should be created in the check_input function
# implement a recursive function to solve the equation
