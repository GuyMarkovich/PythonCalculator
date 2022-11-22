# operator dictionary
opDict = {  # Priority for all operands, numbers should hold priority  0
    '+': 1, '-': 1,
    '*': 2, '/': 2,
    '^': 3, '%': 4,
    '$': 5, '&': 5, '@': 5,
    '~': 6, '!': 6,
    '(': 10, ')': 10
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
                raise ValueError(f"Space at index: {index_num} is invalid, whitespace cannot be between two operands")
        index_num += 1

    # if no error raised so far remove all spaces
    index_num = 0
    while index_num < len(input_list):
        if input_list[index_num][0] == ' ':
            input_list.pop(index_num)
        index_num += 1


def main():
    # receive equation from user:
    raw_input = input("Input your equation here: ")

    input_lst = []

    # categorize  input by priority and category, list holds a list of these attributes for each character
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

    # identify invalid input and remove spaces
    try:
        identify_garbage(input_lst)
        remove_spaces(input_lst)

        print(input_lst)  # print updated input if no invalid input found for testing purposes
    except ValueError as e:
        print(e)


if __name__ == '__main__':
    main()
