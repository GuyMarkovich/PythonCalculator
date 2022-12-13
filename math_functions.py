# functions that get passed operands and return the result of the operation
import globals
from globals import *
from classes import *


# +
def addition(a, b):
    return a + b


# -
def subtraction(a, b):
    return a - b


# *
def multiplication(a, b):
    res = a * b
    if res > 9223372036854775807:
        raise OverflowError("The result of the multiplication is too large")
    else:
        return res


# /
def division(a, b):
    if b == 0:
        raise ZeroDivisionError("Division by zero is not allowed")
    else:
        return a / b


# ^
def power(a, b):
    res = pow(a, b)
    if res > 9223372036854775807:
        raise OverflowError("The result of the multiplication is too large")
    else:
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
    if a < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    elif a > 170:
        raise OverflowError("The result of the factorial is too large")
    elif a == 0:
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


def calculate_binary(op1, op2, operator):
    """function that calculates the result of an operation"""
    op1 = float(op1)
    op2 = float(op2)
    if operator == '+':
        return addition(op1, op2)
    elif operator == '-':
        return subtraction(op1, op2)
    elif operator == '*':
        return multiplication(op1, op2)
    elif operator == '/':
        return division(op1, op2)
    elif operator == '^':
        return power(op1, op2)
    elif operator == '%':
        return modulo(op1, op2)
    elif operator == '$':
        return maximum(op1, op2)
    elif operator == '&':
        return minimum(op1, op2)
    elif operator == '@':
        return average(op1, op2)


def calculate_unary(op1, operator):
    """function that calculates the result of an operation"""
    op1 = float(op1)
    if operator == '~':
        return tilde(op1)
    elif operator == '!':
        return factorial(op1)
    elif operator == '#':
        return sum_of_digits(op1)


def get_result(curr_equation: Equation):
    """function that calculates the result of an equation"""
    eq_len = len(curr_equation.equation)
    i = 0
    while eq_len > 1:
        if curr_equation.equation[i][0] in globals.allOps:
            if curr_equation.equation[i][0] in globals.binOps:
                curr_equation.equation[i][0] = str(calculate_binary(curr_equation.equation[i - 2][0],
                                                                    curr_equation.equation[i - 1][0],
                                                                    curr_equation.equation[i][0]))
                eq_len -= 2

                curr_equation.equation.pop(i - 1)
                curr_equation.equation.pop(i - 2)

                i = i - 2
            elif curr_equation.equation[i][0] in globals.rightUnOps:
                curr_equation.equation[i][0] = str(calculate_unary(curr_equation.equation[i - 1][0],
                                                                   curr_equation.equation[i][0]))
                eq_len -= 1

                curr_equation.equation.pop(i - 1)

                i = i - 1
            elif curr_equation.equation[i][0] in globals.leftUnOps:
                curr_equation.equation[i][0] = str(calculate_unary(curr_equation.equation[i - 1][0],
                                                                   curr_equation.equation[i][0]))
                eq_len -= 1

                curr_equation.equation.pop(i - 1)

                i = i - 1
        i += 1

    return curr_equation
