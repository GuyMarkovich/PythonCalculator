# operator dictionary
opDict = {  # Priority for all operands, numbers hold priority  0
    '+': 1, '-': 1,
    '*': 2, '/': 2,
    '^': 3, '%': 4,
    '$': 5, '&': 5, '@': 5,
    '~': 6, '!': 6, '#': 6,
    '(': 10, ')': 10,
    '.': 0
}

# binary operators
binOps = ['+', '-', '*', '/', '^', '%', '$', '&', '@', '.']
# right unary operators
rightUnOps = ['!', '#']
# left unary operators
leftUnOps = ['~']
