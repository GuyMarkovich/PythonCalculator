# functions that get passed operands and return the result of the operation

# +
def addition(a, b):
    return a + b


# -
def subtraction(a, b):
    return a - b


# *
def multiplication(a, b):
    return a * b


# /
def division(a, b):
    return a / b


# ^
def power(a, b):
    return pow(a, b)


# %
def modulo(a, b):
    return a % b


# $ (maximum)
def maximum(a, b):
    if a > b:
        return a
    else:
        return b


# & (minimum)
def minimum(a, b):
    if a < b:
        return a
    else:
        return b


# @ (average)
def average(a, b):
    return (a + b) / 2


# ~ (change sign)
def tilde(a):
    return a * (-1)


# ! (factorial)
def factorial(a):
    if a == 0:
        return 1
    else:
        return a * factorial(a - 1)


# # sum of digits
def sum_of_digits(a):
    minus_sign = 1
    # if a is a negative number, make it positive and add a minus sign to the result
    if a < 0:
        a = a * (-1)
        minus_sign = -1
    digit_sum = 0
    while a > 0:
        digit_sum += a % 10
        a = int(a / 10)
    return digit_sum * minus_sign
