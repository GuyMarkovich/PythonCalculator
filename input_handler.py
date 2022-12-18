import globals
from globals import *
from classes import *
from math_functions import *


def append_operator(curr_equation: Equation, temp_lst):
    """function for appending operators to the equation list as postfix"""
    # if operator stack is empty, push into the stack
    if len(curr_equation.operator_stack) == 0:
        curr_equation.operator_stack.append(temp_lst)
    else:
        # if the operator on top of the stack has a higher precedence than the current operator, pop the operator
        # from the stack and append it to the equation list
        if temp_lst[0] in globals.allOps:
            while (len(curr_equation.equation) != 0) and (len(curr_equation.operator_stack) != 0) \
                    and (curr_equation.operator_stack[len(curr_equation.operator_stack) - 1][2] >= temp_lst[2]):
                curr_equation.equation.append(curr_equation.operator_stack.pop())
            curr_equation.operator_stack.append(temp_lst)
        elif temp_lst[0] == '(':
            curr_equation.operator_stack.append(temp_lst)
        elif temp_lst[0] == ')':
            # pop operators from the stack and append them to the equation list until an open parenthesis is found
            while curr_equation.operator_stack[len(curr_equation.operator_stack) - 1][0] != '(':
                curr_equation.equation.append(curr_equation.operator_stack.pop())
            # pop the open parenthesis from the stack
            curr_equation.operator_stack.pop()


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
        # if the equation is empty, or the previous non-minus char is a binary op the minus sign is a left unary
        # operator
        if len(curr_equation.equation) == 0 or cnt_holder.pre_minus_char in globals.binOps:
            # if the next character after minus is parenthesis, it is a left unary operator,
            # and we can append a tilde if number of minuses is odd
            if raw_input[index] == '(':
                if cnt_holder.get_minus_cnt() % 2 == 1:
                    temp_lst = ['~', 'operator', opDict['~'] + cnt_holder.get_parentheses_multiplier()]
                    append_operator(curr_equation, temp_lst)
                    cnt_holder.reset_minus_cnt()
            # if not parenthesis, we can add a minus to the operand
            else:
                # if number of minuses is odd, append a minus to the operand, else there's no need to append anything
                if cnt_holder.get_minus_cnt() % 2 == 1 and op_str.get_op_str() != '':
                    op_str.add_to_beginning('-')
                    cnt_holder.reset_minus_cnt()
        # if the equation is not empty and the minus is between two operands,
        # one minus is a left unary character and the rest are a binary operator
        elif (cnt_holder.pre_minus_char in globals.operands or cnt_holder.pre_minus_char == ')') and \
                (raw_input[index] in globals.operands or raw_input[index] == '('):
            # if current char is left unary, no need to take one minus to the operand
            if raw_input[index] in leftUnOps:
                if cnt_holder.get_minus_cnt() % 2 == 1:
                    temp_lst = ['-', 'operator', opDict['-'] + cnt_holder.get_parentheses_multiplier()]
                    append_operator(curr_equation, temp_lst)
                    cnt_holder.reset_minus_cnt()
                else:
                    temp_lst = ['+', 'operator', opDict['+'] + cnt_holder.get_parentheses_multiplier()]
                    append_operator(curr_equation, temp_lst)
                    cnt_holder.reset_minus_cnt()
            else:
                if (cnt_holder.get_minus_cnt() - 1) % 2 == 1:
                    temp_lst = ['-', 'operator', opDict['-'] + cnt_holder.get_parentheses_multiplier()]
                    append_operator(curr_equation, temp_lst)
                    cnt_holder.reset_minus_cnt()
                    if raw_input[index] == '(':
                        temp_lst = ['~', 'operator', opDict['~'] + cnt_holder.get_parentheses_multiplier()]
                        append_operator(curr_equation, temp_lst)
                        cnt_holder.reset_minus_cnt()
                    else:
                        op_str.add_to_beginning('-')
                        cnt_holder.reset_minus_cnt()
                else:  # number of minuses -1 is even, append a plus and one minus or tilde if needed
                    temp_lst = ['+', 'operator', opDict['-'] + cnt_holder.get_parentheses_multiplier()]
                    append_operator(curr_equation, temp_lst)
                    cnt_holder.reset_minus_cnt()
                    if raw_input[index] == '(':
                        temp_lst = ['~', 'operator', opDict['~'] + cnt_holder.get_parentheses_multiplier()]
                        append_operator(curr_equation, temp_lst)
                        cnt_holder.reset_minus_cnt()
                    else:
                        op_str.add_to_beginning('-')
                        cnt_holder.reset_minus_cnt()
    # in case of one minus sign
    elif cnt_holder.get_minus_cnt() == 1:
        # if the equation is empty, or the previous non-minus char is a binary op the minus sign is a left unary
        # operator
        if len(curr_equation.equation) == 0 or cnt_holder.pre_minus_char in globals.binOps:
            # if the next character after minus is parenthesis, it is a left unary operator, and we can append a tilde
            if raw_input[index] == '(':
                temp_lst = ['~', 'operator', opDict['~'] + cnt_holder.get_parentheses_multiplier()]
                append_operator(curr_equation, temp_lst)
                cnt_holder.reset_minus_cnt()
            # if not parenthesis, we can add a minus to the operand
            else:
                if op_str.get_op_str() != '':
                    op_str.add_to_beginning('-')
                    cnt_holder.reset_minus_cnt()
        # if the minus is between two operands it is a binary operator
        elif (cnt_holder.pre_minus_char in globals.operands or cnt_holder.pre_minus_char == ')'
              or cnt_holder.pre_minus_char in globals.rightUnOps) and \
                (raw_input[index] in globals.operands or raw_input[index] == '(' or raw_input[index] in leftUnOps):
            temp_lst = ['-', 'operator', opDict['-'] + cnt_holder.get_parentheses_multiplier()]
            append_operator(curr_equation, temp_lst)
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
            # remember the last non-minus character
            if index != 0:
                if raw_input[index - 1] != '-':
                    cnt_holder.set_pre_minus_char(raw_input[index - 1])
            cnt_holder.inc_minus_cnt()
        # decimal should be appended to the operand string and not as a binary operator
        elif raw_input[index] == '.':
            op_str.add_to_op_str(raw_input[index])
        else:
            temp_lst = [raw_input[index], 'operator',
                        opDict[raw_input[index]] + cnt_holder.get_parentheses_multiplier()]
            append_operator(curr_equation, temp_lst)


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
    elif index != 0 and raw_input[index - 1] not in binOps and raw_input[index - 1] != '(' \
            and raw_input[index - 1] not in leftUnOps:
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

        # since a left unary operator can appear after a minus we need to append any previously counted minus signs,
        # but because tilde has higher priority, if the minus is unary the minus will only be appended on the result
        # of the tilde for this we will use the internal operator '_', it will only be used in this special case
        if len(curr_equation.equation) == 0:
            if cnt_holder.get_minus_cnt() > 0:
                if cnt_holder.get_minus_cnt() % 2 == 1:
                    temp_lst = ['_', 'operator', opDict['_'] + cnt_holder.get_parentheses_multiplier()]
                    append_operator(curr_equation, temp_lst)
                cnt_holder.reset_minus_cnt()
        else:
            append_minus(raw_input, index, curr_equation, cnt_holder, op_str)

        temp_lst = [raw_input[index], 'operator', opDict[raw_input[index]] + cnt_holder.parentheses_multiplier]
        append_operator(curr_equation, temp_lst)


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
        append_operator(curr_equation, temp_lst)


def check_allOps(index, raw_input, curr_equation, cnt_holder, op_str):
    """divide all operators into their respective categories"""
    if raw_input[index] in binOps:
        check_binOps(index, raw_input, curr_equation, cnt_holder, op_str)
        return
    elif raw_input[index] in rightUnOps:
        check_rightUnOps(index, raw_input, curr_equation, cnt_holder)
        return
    elif raw_input[index] in user_leftUnOps:
        check_leftUnOps(index, raw_input, curr_equation, cnt_holder, op_str)
        return
    else:
        raise SyntaxError(f"Invalid character: {raw_input[index]} in equation at index {index}, character is not a "
                          f"valid operator")


# check if input is valid
# if not, return error message
# else, return new equation without unnecessary characters
def check_input(raw_input, curr_equation, op_str, cnt_holder: CounterHolder):
    """check if user input is valid"""

    index = 0
    for i in raw_input:
        if i in operands:
            # add operand to the string
            op_str.add_to_op_str(raw_input[index])
            # append any previously counted minus signs
            append_minus(raw_input, index, curr_equation, cnt_holder, op_str)
            index += 1
        elif i in allOps:
            # if operator is a decimal point no need to get rid of the stored operand string
            # before adding it to the number
            if i != '.':
                append_operand(op_str, curr_equation, cnt_holder)

            check_allOps(index, raw_input, curr_equation, cnt_holder, op_str)
            index += 1
        elif i == '(':
            # append any previously counted minus signs
            append_minus(raw_input, index, curr_equation, cnt_holder, op_str)
            # if the previous character is a number or a right unary operator throw a syntax error
            if index != 0 and (raw_input[index - 1] in operands or raw_input[index - 1] in rightUnOps):
                raise SyntaxError(f"Invalid character: {raw_input[index]} in equation at index {index}, open "
                                  f"parenthesis cannot follow a number or a right unary operator")

            cnt_holder.tilde_reset()  # reset tilde count when open parenthesis is appended
            temp_lst = [raw_input[index], 'operator',
                        opDict[raw_input[index]] + cnt_holder.get_parentheses_multiplier()]
            cnt_holder.parentheses_multiplier += 10
            append_operator(curr_equation, temp_lst)
            index += 1
        elif i == ')':
            if cnt_holder.get_parentheses_multiplier() == 0:
                raise SyntaxError(f"Invalid character: {raw_input[index]} in equation at index {index}, closed "
                                  f"parenthesis cannot be placed before an open parenthesis")
            append_operand(op_str, curr_equation, cnt_holder)

            cnt_holder.parentheses_multiplier -= 10
            temp_lst = [raw_input[index], 'operator',
                        opDict[raw_input[index]] + cnt_holder.get_parentheses_multiplier()]
            append_operator(curr_equation, temp_lst)
            index += 1
        else:
            raise SyntaxError(f"Invalid character: {raw_input[index]} in equation at index {index}")
    # append last operand to the new equation if exists
    if index == len(raw_input):
        append_operand(op_str, curr_equation, cnt_holder)
    if cnt_holder.get_parentheses_multiplier() != 0:
        raise SyntaxError("Parentheses unbalanced")

    while curr_equation.operator_stack:
        curr_equation.equation.append(curr_equation.operator_stack.pop())
    return curr_equation


def calculate_equation(equation):
    # object that holds multiple counters and anything that needs to be transferred between functions:
    cnt_holder = CounterHolder()
    op_str = OpString('')  # string to hold the operators, temporary variable to be used in the check_input function
    curr_equation = Equation()  # equation object to hold the equation
    result = 0  # to store the result of the equation
    # equation received from the user
    raw_input = equation
    # strip all whitespace from the equation
    raw_input = raw_input.replace(' ', '')
    raw_input = raw_input.replace('\t', '')

    # if equation is empty, return 0
    if raw_input == '':
        return result

    try:
        # check if input is valid
        curr_equation = check_input(raw_input, curr_equation, op_str, cnt_holder)
        # test print of the post-fix equation
        # print(curr_equation.equation)
    except SyntaxError as e:
        print(e)
        print("Your equation: " + raw_input)
        result = "Error"  # if an error is thrown, return "Error"
        return result
    try:
        # calculate the equation
        curr_equation = get_result(curr_equation)
        # print(curr_equation.equation) - test print of the equation after calculation
    except ZeroDivisionError as e:
        print(e)
        print("Your equation: " + raw_input)
        result = "Error"
    except ValueError as e:
        print(e)
        print("Your equation: " + raw_input)
        result = "Error"
    except OverflowError as e:
        print(e)
        print("Your equation: " + raw_input)
        result = "Error"

    if result != "Error": #if no errors encountered print result
        result = float(curr_equation.equation.pop()[0])
    return result
