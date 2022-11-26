# operator dictionary
opDict = {  # Priority for all operands, numbers hold priority  0
    '+': 1, '-': 1,
    '*': 2, '/': 2,
    '^': 3, '%': 4,
    '$': 5, '&': 5, '@': 5,
    '~': 6, '!': 6,
    '(': 10, ')': 10,
    '.': 0
}


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
            # if parenthesis are balanced return input_list
            return input_list


# tilda check
def check_tilda(input_list):
    # if no tilda is present return input_list
    tilda_cnt = 0
    for index in input_list:
        if index[0] == '~':
            tilda_cnt = tilda_cnt + 1
    if tilda_cnt == 0:
        return input_list

    # if tilda is last element in input_list raise syntax error
    if input_list[-1][0] == '~':
        raise SyntaxError(f"Tilda at index: {len(input_list) - 1} is invalid, cannot be last element in input,"
                          f" must appear before operand")
    # if tilda after operand or exclamation mark raise syntax error
    index_num = 1
    while index_num < len(input_list) - 1:
        if input_list[index_num][0] == '~':
            if input_list[index_num - 1][1] == "operand" or input_list[index_num - 1][0] == '!':
                raise SyntaxError(f"Tilda at index: {index_num} is invalid, cannot be after an operand or exclamation mark")
        index_num += 1

    # if tilda is not followed by an operand or minus raise syntax error
    index_num = 0
    while index_num < len(input_list) - 1:
        if input_list[index_num][0] == '~':
            if input_list[index_num + 1][1] != "operand" and input_list[index_num + 1][0] != '-' \
                    and input_list[index_num + 1][0] != '~':
                # the line above allows invalid input (tilda after tilda) for
                # the purpose of throwing an appropriate error in the next check
                raise SyntaxError(f"Tilda at index: {index_num} is invalid, must be followed by an operand or minus")
        index_num += 1

    # if after a tilda and before an operand there is another tilda raise syntax error
    index_num = 0
    while index_num < len(input_list) - 1:
        if input_list[index_num][0] == '~':
            while input_list[index_num + 1][1] != 'operand':
                if input_list[index_num + 1][0] == '~':
                    raise SyntaxError(f"Tilda at index: {index_num + 1} is invalid, cannot be after another tilda")
                index_num += 1
        index_num += 1


# check ! operator
def check_exclamation(input_list):
    # if no exclamation is present return input_list
    exclamation_cnt = 0
    for index in input_list:
        if index[0] == '!':
            exclamation_cnt = exclamation_cnt + 1
    if exclamation_cnt == 0:
        return input_list
    # if exclamation is first element in input_list raise syntax error
    if input_list[0][0] == '!':
        raise SyntaxError(f"Exclamation at index: 0 is invalid, cannot be first element in input,"
                          f" must appear after operand or right parenthesis")
    # exclamation must follow an operand or right parenthesis, otherwise raise syntax error
    index_num = 0
    while index_num < len(input_list) - 1:
        if input_list[index_num][0] == '!':
            if input_list[index_num - 1][1] != "operand" and input_list[index_num - 1][0] != ')':
                raise SyntaxError(
                    f"Exclamation at index: {index_num} is invalid, must be preceded by an operand or right parenthesis")
        index_num += 1


# main for testing purposes, should be moved to a separate file that is responsible for calculations
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
        # check parenthesis are balanced
        check_parenthesis(input_lst)
        # remove unnecessary spaces and tabs and identify inappropriate spaces and tabs
        remove_spaces(input_lst)
        # remove excess minuses
        remove_minuses(input_lst)
        # check if tilda in function located in valid position
        check_tilda(input_lst)
        # check exclamation
        check_exclamation(input_lst)

        print(input_lst)  # print updated input if no invalid input found for testing purposes
    except (ValueError, SyntaxError) as e:
        print(e)


if __name__ == '__main__':
    main()
