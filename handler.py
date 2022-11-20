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

try:
    identify_garbage(input_lst)

    print(input_lst)
except ValueError as e:
    print(e)

print ("test")
