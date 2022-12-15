from math_functions import *

# operator dictionary
opDict = {  # Priority for all operands, numbers hold priority  0
    '+': 1, '-': 1,
    '*': 2, '/': 2,
    '^': 3, '%': 4,
    '$': 5, '&': 5, '@': 5, '_': 5.9,  # _ is the unary minus operator for internal use for when a unary minus is
    # used before a tilde
    '~': 6, '!': 6, '#': 6,
    '(': 10, ')': 10,
    '.': 0
}

# operands tuple
operands = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
# tuple of allowed spaces
spaces = (' ', '\t')

# binary operators
binOps = ['+', '-', '*', '/', '^', '%', '$', '&', '@', '.']
# right unary operators
rightUnOps = ['!', '#']
# left unary operators
leftUnOps = ['~', '_']
user_leftUnOps = ['~']  # left unary operators that the user can use
# (to prevent the user from using the underscore operator)

# all operators
allOps = binOps + rightUnOps + leftUnOps
