from globals import *
from classes import *


def append_operand(op_str, input_lst, cnt_holder):
    if op_str.get_op_str() != '':
        temp_lst = [op_str.get_op_str(), 'operand', 0]
        input_lst.append(temp_lst)
        # reset operand string
        op_str.empty_op_str()
        # reset tilde count when operand is appended
        cnt_holder.tilde_reset()


def append_minus(input_lst, cnt_holder, op_str):
    if cnt_holder.get_minus_cnt() > 0:
        # if list is previously empty, the minus sign is a left unary operator
        if len(input_lst) == 0:
            if cnt_holder.get_minus_cnt() % 2 == 1:
                op_str.add_to_beginning('-')
                cnt_holder.reset_minus_cnt()
            else:
                cnt_holder.reset_minus_cnt()
        # if last character on list is a binary operator the minus is a left unary operator
        elif input_lst[len(input_lst) - 1][0] in binOps:
            if cnt_holder.get_minus_cnt() % 2 == 1:
                op_str.add_to_beginning('-')
                cnt_holder.reset_minus_cnt()
            else:
                cnt_holder.reset_minus_cnt()
        else:
            if (cnt_holder.get_minus_cnt() - 1) % 2 == 1:
                temp_lst = ['-', 'operator', opDict['-'] + cnt_holder.get_parentheses_multiplier()]
                input_lst.append(temp_lst)
                cnt_holder.reset_minus_cnt()
                op_str.add_to_beginning('-')
                cnt_holder.reset_minus_cnt()
            else:
                temp_lst = ['+', 'operator', opDict['+'] + cnt_holder.get_parentheses_multiplier()]
                input_lst.append(temp_lst)
                cnt_holder.reset_minus_cnt()
                op_str.add_to_beginning('-')
                cnt_holder.reset_minus_cnt()


def check_binOps(index, raw_input, input_lst, cnt_holder):
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
    # if passed all checks, append to input_lst
    else:
        if raw_input[index] == '-':
            cnt_holder.inc_minus_cnt()
        else:
            temp_lst = [raw_input[index], 'operator',
                        opDict[raw_input[index]] + cnt_holder.get_parentheses_multiplier()]
            input_lst.append(temp_lst)


def check_leftUnOps(index, raw_input, input_lst, cnt_holder, op_str):
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
    # if passed all checks, append to input_lst
    else:
        # if operator is a tilde (~), increment tilde count
        if raw_input[index] == '~':
            cnt_holder.inc_tilde_cnt()
        # if tilde count is more than 1, throw a syntax error
        if cnt_holder.get_tilde_cnt() > 1:
            raise SyntaxError(f"Invalid character: {raw_input[index]} in equation at index {index}, tilde (~) "
                              f"cannot be used more than once on one operand")

        # since a left unary operator can appear before a minus we need to append any previously counted minus signs
        append_minus(input_lst, cnt_holder, op_str)

        temp_lst = [raw_input[index], 'operator', opDict[raw_input[index]] + cnt_holder.parentheses_multiplier]
        input_lst.append(temp_lst)


def check_rightUnOps(index, raw_input, input_lst, cnt_holder):
    if index == 0:
        raise SyntaxError(
            f"Invalid character: {raw_input[index]} in equation at index {index}, right unary operator cannot be "
            f"first character")
    # if the previous character is not an operator or an open parenthesis, throw a syntax error
    elif raw_input[index - 1] not in operands and raw_input[index - 1] != ')' \
            and raw_input[index - 1] not in rightUnOps:
        raise SyntaxError(f"Invalid character: {raw_input[index]} in equation at index {index}")
    # if next character is not a binary operator, or a right unary operator, or a closed parenthesis, throw a syntax
    # error
    elif index != len(raw_input) - 1 and raw_input[index + 1] not in binOps and raw_input[index + 1] not in rightUnOps \
            and raw_input[index + 1] != ')':
        raise SyntaxError(f"Invalid character: {raw_input[index]} in equation at index {index}, right unary operator "
                          f"must be followed by a binary operator, another right unary operator, or a closed "
                          f"parenthesis")
    # if passed all checks, append to input_lst
    else:
        temp_lst = [raw_input[index], 'operator', opDict[raw_input[index]] + cnt_holder.get_parentheses_multiplier()]
        input_lst.append(temp_lst)


def check_allOps(index, raw_input, input_lst, cnt_holder, operand_str):
    """divide all operators into their respective categories"""
    if raw_input[index] in binOps:
        check_binOps(index, raw_input, input_lst, cnt_holder)
        return
    elif raw_input[index] in rightUnOps:
        check_rightUnOps(index, raw_input, input_lst, cnt_holder)
        return
    elif raw_input[index] in leftUnOps:
        check_leftUnOps(index, raw_input, input_lst, cnt_holder, operand_str)
        return


# check if input is valid
# if not, return error message
# else, return new equation without unnecessary characters
def check_input(raw_input, input_lst, op_str, cnt_holder: CounterHolder):
    """check if user input is valid"""
    # remove all spaces and tabs
    raw_input = raw_input.replace(' ', '')
    raw_input = raw_input.replace('\t', '')

    index = 0
    for i in raw_input:
        if i in operands:
            # append any previously counted minus signs
            append_minus(input_lst, cnt_holder, op_str)
            # add operand to the string
            op_str.add_to_op_str(raw_input[index])
            index += 1
        elif i in allOps:
            append_operand(op_str, input_lst, cnt_holder)

            check_allOps(index, raw_input, input_lst, cnt_holder, op_str)
            index += 1
        elif i == '(':
            # if the previous character is a number or a right unary operator throw a syntax error
            if index != 0 and (raw_input[index - 1] in operands or raw_input[index - 1] in rightUnOps):
                raise SyntaxError(f"Invalid character: {raw_input[index]} in equation at index {index}, open "
                                  f"parenthesis cannot follow a number or a right unary operator")

            cnt_holder.tilde_reset()  # reset tilde count when open parenthesis is appended
            cnt_holder.parentheses_multiplier += 10
            temp_lst = [raw_input[index], 'operator',
                        opDict[raw_input[index]] + cnt_holder.get_parentheses_multiplier()]
            input_lst.append(temp_lst)
            index += 1
        elif i == ')':

            append_operand(op_str, input_lst, cnt_holder)

            temp_lst = [raw_input[index], 'operator',
                        opDict[raw_input[index]] + cnt_holder.get_parentheses_multiplier()]
            cnt_holder.parentheses_multiplier -= 10
            input_lst.append(temp_lst)
            index += 1
        else:
            raise SyntaxError(f"Invalid character: {raw_input[index]} in equation at index {index}")
    # append last operand to the new equation if exists
    if index == len(raw_input):
        append_operand(op_str, input_lst, cnt_holder)
    if cnt_holder.get_parentheses_multiplier() != 0:
        raise SyntaxError("Parentheses unbalanced")

    return input_lst


def main():
    cnt_holder = CounterHolder()

    operand_str = ''  # string to hold the operands, temporary variable to be used in the check_input function
    op_str = OpString('')  # string to hold the operators, temporary variable to be used in the check_input function

    # receive equation from user:
    raw_input = input("Input your equation here: ")
    input_lst = []  # list will hold the modified equation
    try:
        input_lst = check_input(raw_input, input_lst, op_str, cnt_holder)
        print(raw_input)
        print(input_lst)
    except SyntaxError as e:
        print(e)
        print("Your equation: " + raw_input)
        exit(1)


if __name__ == '__main__':
    main()
