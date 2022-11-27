from globals import *


def identify_garbage(input_list):
    """Identifies invalid input, does not check syntax correctness for valid input"""
    index_num = 0  # tracks index
    for index in input_list:
        if index[2] == -1:
            if index[0] != ' ' and index[0] != '\t':
                raise ValueError(f"Char at index: {index_num} is invalid")
        index_num += 1


def remove_spaces(input_list):
    """function to remove unnecessary spaces and tabs, also checks for invalid spaces and tabs"""
    # if no spaces or tabs are present, return input_list
    space_cnt = 0
    for index in input_list:
        if index[0] == ' ' or index[0] == '\t':
            space_cnt = space_cnt + 1

    if space_cnt == 0:
        return input_list

    # remove spaces and tabs from input before the first operand or operator
    while input_list[0][0] == ' ' or input_list[0][0] == '\t':
        input_list.pop(0)
    # remove spaces and tabs from input after the last operand or operator
    while input_list[-1][0] == ' ' or input_list[-1][0] == '\t':
        input_list.pop(-1)

    # convert tabs to spaces
    for index in input_list:
        if index[0] == '\t':
            index[0] = ' '

    # if multiple spaces in a row, remove all but one
    index_num = 0
    while index_num < len(input_list):
        if input_list[index_num][0] == ' ':
            while input_list[index_num + 1][0] == ' ':
                input_list.pop(index_num + 1)
        index_num += 1

    # if whitespace between two operands raise value error
    index_num = 1
    while index_num < len(input_list) - 1:
        if input_list[index_num][0] == ' ':
            if input_list[index_num - 1][1] == "operand" and input_list[index_num + 1][1] == "operand":
                raise SyntaxError(f"Space at index: {index_num} is invalid, whitespace cannot be between two operands")
        index_num += 1

    # if no error raised so far remove all spaces
    index_num = 0
    while index_num < len(input_list):
        if input_list[index_num][0] == ' ':
            input_list.pop(index_num)
        index_num += 1


def remove_minuses(input_list):
    """Function to remove excess minuses"""
    # if not minuses are present return input_list
    minus_cnt = 0
    for index in input_list:
        if index[0] == '-':
            minus_cnt = minus_cnt + 1
    if minus_cnt == 0:
        return input_list

    # if minus is last element in input_list raise syntax error
    if input_list[-1][0] == '-':
        raise SyntaxError(f"Minus at index: {len(input_list) - 1} is invalid, cannot be last element in input")

    # if multiple minuses in a row at start of input, if number of minuses even, remove all, if odd replace all with 1
    # minus
    index_num = 0
    if input_list[0][0] == '-':
        minus_cnt = 0
        while input_list[0][0] == '-':
            minus_cnt = minus_cnt + 1
            input_list.pop(0)
        if minus_cnt % 2 == 1:
            input_list.insert(0, ['-', 'operator', 1])

    # if multiple minuses in a row after an operator other than minus, if number of minuses even, remove all,
    # if odd replace all with 1 minus
    index_num = 1
    while index_num < len(input_list) - 1:
        if input_list[index_num][0] == '-':
            if input_list[index_num - 1][1] == 'operator' and input_list[index_num - 1][0] != '-':
                minus_cnt = 0
                while input_list[index_num][0] == '-':
                    minus_cnt = minus_cnt + 1
                    input_list.pop(index_num)
                if minus_cnt % 2 == 1:
                    input_list.insert(index_num, ['-', 'operator', 1])
        index_num += 1

    # if multiple minuses after an operand, if number of minuses even, replace with one plus, if odd replace all with
    # 1 minus
    index_num = 1
    while index_num < len(input_list) - 1:
        if input_list[index_num][0] == '-':
            if input_list[index_num - 1][1] == 'operand':
                minus_cnt = 0
                while input_list[index_num][0] == '-':
                    minus_cnt = minus_cnt + 1
                    input_list.pop(index_num)
                if minus_cnt % 2 == 1:
                    input_list.insert(index_num, ['-', 'operator', 1])
                else:
                    input_list.insert(index_num, ['+', 'operator', 1])
        index_num += 1


# check parenthesis
def check_parenthesis(input_list):
    """function to check if parenthesis are balanced"""
    # count all appearances of parenthesis
    right_parenthesis_cnt = 0
    left_parenthesis_cnt = 0
    for index in input_list:
        if index[0] == '(':
            left_parenthesis_cnt = left_parenthesis_cnt + 1
        elif index[0] == ')':
            right_parenthesis_cnt = right_parenthesis_cnt + 1
    # if no parenthesis are present return input_list
    if right_parenthesis_cnt == 0 and left_parenthesis_cnt == 0:
        return input_list
    else:
        # if number of left parenthesis is not equal to number of right parenthesis raise syntax error
        if right_parenthesis_cnt > left_parenthesis_cnt:
            raise SyntaxError("Parenthesis are not balanced, missing left parenthesis")
        elif right_parenthesis_cnt < left_parenthesis_cnt:
            raise SyntaxError("Parenthesis are not balanced, missing right parenthesis")
        else:
            # left parenthesis cannot be last element in input_list
            if input_list[-1][0] == '(':
                raise SyntaxError("Left parenthesis cannot be last element in input")
            # right parenthesis cannot be first element in input_list
            if input_list[0][0] == ')':
                raise SyntaxError("Right parenthesis cannot be first element in input")
            # if left parenthesis is followed by right parenthesis raise syntax error
            index_num = 0
            while index_num < len(input_list) - 1:
                if input_list[index_num][0] == '(' and input_list[index_num + 1][0] == ')':
                    raise SyntaxError(f"Parenthesis at index: {index_num} invalid, cannot be empty")
                index_num += 1
            # left parenthesis must follow a binary operator or be the first element in input_list
            index_num = 0
            while index_num < len(input_list):
                if input_list[index_num][0] == '(':
                    if index_num != 0:
                        if input_list[index_num - 1][0] not in binOps:
                            raise SyntaxError(
                                f"Parenthesis at index: {index_num} invalid, must follow a binary operator")
                index_num += 1
            # right parenthesis must follow an operand or be the last element in input_list
            index_num = 0
            while index_num < len(input_list):
                if input_list[index_num][0] == ')':
                    if input_list[index_num - 1][1] != 'operand':
                        raise SyntaxError(
                            f"Parenthesis at index: {index_num} invalid, must follow an operand")
                index_num += 1


# check left unary operators
def check_left_unary(input_list):
    # if no left unary operators are present return input_list
    left_unary_cnt = 0
    for index in input_list:
        if index[0] in leftUnOps:  # if index[0] is a left unary operator
            left_unary_cnt = left_unary_cnt + 1  # update counter
    if left_unary_cnt == 0:
        return input_list
    # left unary operators cannot follow an operand or right parenthesis
    index_num = 1
    while index_num < len(input_list):
        if input_list[index_num][0] in leftUnOps:
            if input_list[index_num - 1][1] == 'operand' or input_list[index_num - 1][0] == ')':
                raise SyntaxError(
                    f"Operator: {input_list[index_num][0]} at index: {index_num} is invalid, cannot follow an operand or right "
                    f"parenthesis")
        index_num += 1
    # left unary operators cannot be last element in input_list
    if input_list[-1][0] in leftUnOps:
        raise SyntaxError(
            f"Operator: {input_list[-1][0]} at index: {len(input_list) - 1} is invalid, cannot be last element in input")
    # left unary operators must be followed by an operand or minus or left parenthesis
    index_num = 0
    while index_num < len(input_list) - 1:
        if input_list[index_num][0] in leftUnOps:
            if input_list[index_num + 1][1] != 'operand' and input_list[index_num + 1][0] != '-' \
                    and input_list[index_num + 1][0] != '(':
                raise SyntaxError(
                    f"Operator: {input_list[index_num][0]} at index: {index_num} is invalid, must be followed by an "
                    f"operand, minus or left parenthesis")
        index_num += 1


# check right unary operators
def check_right_unary(input_list):
    # if no right unary operators are present return input_list
    right_unary_cnt = 0
    for index in input_list:
        if index[0] in rightUnOps:
            right_unary_cnt = right_unary_cnt + 1
    if right_unary_cnt == 0:
        return input_list
    # if right unary operator is first element in input_list raise syntax error
    if input_list[0][0] in rightUnOps:
        raise SyntaxError(f"Operator: {input_list[0][0]} at index: 0 is invalid, cannot be first element in input,"
                          f" must appear after operand or right parenthesis")
    # right unary operator must follow an operand or right parenthesis, otherwise raise syntax error
    list_index = 0
    while list_index < len(input_list) - 1:
        if input_list[list_index][0] in rightUnOps:
            if input_list[list_index - 1][1] != "operand" and input_list[list_index - 1][0] != ')':
                raise SyntaxError(
                    f"Operator: {input_list[list_index][0]} at index: {list_index} is invalid, must be preceded by an "
                    f"operand or right "
                    f"parenthesis")
        list_index += 1
    # right unary operator must be followed by a binary operator,otherwise raise syntax error
    list_index = 0
    while list_index < len(input_list) - 1:
        if input_list[list_index][0] in rightUnOps:
            if input_list[list_index + 1][1] not in binOps:
                raise SyntaxError(
                    f"Operator: {input_list[list_index][0]} at index: {list_index} is invalid, must be followed by a "
                    f"binary operator")
        list_index += 1


# check binary operators
def check_binary(input_list):
    # binary operators cannot be first element in input_list
    if input_list[0][1] in binOps:
        raise SyntaxError(f"Operator: {input_list[0][0]} at index: 0 is invalid, cannot be first element in input")
    # binary operators cannot be last element in input_list
    if input_list[-1][1] in binOps:
        raise SyntaxError(
            f"Operator: {input_list[-1][0]} at index: {len(input_list) - 1} is invalid, cannot be last element in input")
    # binary operators cannot be followed by another binary operator other than minus and left parenthesis
    list_index = 0
    while list_index < len(input_list):
        if input_list[list_index][0] in binOps:
            if input_list[list_index + 1][0] in binOps and input_list[list_index + 1][0] != '-' and \
                    input_list[list_index + 1][0] != '(':
                # special case for decimal point, must be followed by a digit and thus has a different error message
                if input_list[list_index][0] == '.':
                    raise SyntaxError(
                        f"Operator: {input_list[list_index][0]} at index: {list_index} is invalid, must be followed "
                        f"by an "
                        f"operand")
                else:
                    raise SyntaxError(
                        f"Operator: {input_list[list_index][0]} at index: {list_index} is invalid, cannot be followed "
                        f"by another binary operator other than minus and left parenthesis")
        list_index += 1
    # binary operators must be preceded by an operand or right parenthesis
    list_index = 0
    while list_index < len(input_list):
        if input_list[list_index][1] in binOps:
            if input_list[list_index - 1][1] != 'operand' and input_list[list_index - 1][0] != ')':
                raise SyntaxError(
                    f"Operator: {input_list[list_index][0]} at index: {list_index} is invalid, must be preceded by an "
                    f"operand or right parenthesis")
        list_index += 1
    # in case of decimal, check that it isn't followed or preceded by parenthesis
    # if the binary operator is . it must be preceded and followed by an operand
    list_index = 0
    while list_index < len(input_list) - 1:
        if input_list[list_index][0] == '.':
            if input_list[list_index - 1][1] != 'operand' or input_list[list_index + 1][1] != 'operand':
                raise SyntaxError(
                    f"Operator: {input_list[list_index][0]} at index: {list_index} is invalid, decimal must be "
                    f"preceded and followed by an operand")
        list_index += 1


# main for testing purposes, should be moved to a separate functions that completes all checks
def main():
    # receive equation from user:
    raw_input = input("Input your equation here: ")

    input_lst = []

    # categorize  input by priority and type of character, generate map of input
    for element in raw_input:
        temp_list = [element]
        if element.isdigit():
            temp_list.append("operand")
            temp_list.append(0)
        elif element in opDict:
            temp_list.append("operator")
            temp_list.append(opDict.get(element))
        else:
            temp_list.append("unknown")
            temp_list.append(-1)

        input_lst.append(temp_list)

    print(input_lst)  # print original input, testing purposes

    # check validity of input and remove unnecessary characters
    try:
        # identify invalid input
        identify_garbage(input_lst)
        # check parenthesis are balanced and correctly placed
        check_parenthesis(input_lst)
        # remove unnecessary spaces and tabs and identify inappropriate spaces and tabs
        remove_spaces(input_lst)
        # remove excess minuses
        remove_minuses(input_lst)
        # check left unary operators
        check_left_unary(input_lst)
        # check right unary operators
        check_right_unary(input_lst)
        # check binary operators
        check_binary(input_lst)

        print(input_lst)  # print updated input if no invalid input found for testing purposes
    except (ValueError, SyntaxError) as e:
        print(e)


if __name__ == '__main__':
    main()
