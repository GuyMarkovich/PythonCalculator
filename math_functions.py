# functions that get passed operands and return the result of the operation
import globals
from globals import *
from classes import *


# +
def addition(a, b):
    res = a + b
    if res == float('inf'):  # check if value reaches max float
        raise OverflowError("The result of the operation is too large")
    return res


# -
def subtraction(a, b):
    return a - b


# *
def multiplication(a, b):
    res = a * b
    if res == float('inf'):
        raise OverflowError("The result of the operation is too large")
    else:
        if res % 1 == 0:
            res = int(res)
        return res


# /
def division(a, b):
    if b == 0:
        raise ZeroDivisionError("Division by zero is not allowed")
    else:
        res = a / b
        if res % 1 == 0:
            res = int(res)
        return res


# ^ (power)
def power(a, b):
    if a < 0 and b % 1 != 0:
        raise ValueError("Complex numbers are not supported by this calculator")
    res = pow(a, b)
    if res == float('inf'):
        raise OverflowError("The result of the operation is too large")
    if res % 1 == 0:
        res = int(res)

    return res


# % (modulo)
def modulo(a, b):
    if b == 0:
        raise ValueError("Cannot do modulo on 0, illegal operation")
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
    res = (a + b) / 2
    if res % 1 == 0:
        res = int(res)
    return res


# ~ (change sign)
def tilde(a):
    return a * (-1)


# _ (internal unary minus)
def underscore(a):
    return a * (-1)


# ! (factorial)
def factorial(a):
    if a < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    elif a % 1 != 0:
        raise ValueError("Factorial is not defined for non-integer numbers")
    # elif a > 170:
    #   raise OverflowError("The result of the factorial is too large")
    elif a == 0:
        return 1
    else:
        a = int(a)
        return a * factorial(a - 1)


# # sum of digits
def sum_of_digits(a):
    # support for non integer numbers
    while a % 1 != 0:
        a *= 10
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
    # op1 = float(op1)
    # op2 = float(op2)
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
    # op1 = float(op1)
    if operator == '~':
        return tilde(op1)
    elif operator == '!':
        return factorial(op1)
    elif operator == '#':
        return sum_of_digits(op1)
    elif operator == '_':
        return underscore(op1)


def get_result(curr_equation: Equation):
    """function that calculates the result of an equation"""
    eq_len = len(curr_equation.equation)  # get length of equation
    idx = 0  # index of current character
    while eq_len > 1:  # while there are still operators in the equation
        if curr_equation.equation[idx][0] in globals.allOps:
            if curr_equation.equation[idx][0] in globals.binOps:
                # if the operator is a binary operator calculate the result and replace the operator and the operands
                curr_equation.equation[idx][0] = calculate_binary(curr_equation.equation[idx - 2][0],
                                                                  curr_equation.equation[idx - 1][0],
                                                                  curr_equation.equation[idx][0])
                # reduce length of equation by 2
                eq_len -= 2

                # remove the operands used
                curr_equation.equation.pop(idx - 1)
                curr_equation.equation.pop(idx - 2)

                idx = idx - 2
            elif curr_equation.equation[idx][0] in globals.rightUnOps:
                curr_equation.equation[idx][0] = calculate_unary(curr_equation.equation[idx - 1][0],
                                                                 curr_equation.equation[idx][0])
                eq_len -= 1

                # remove the operand used
                curr_equation.equation.pop(idx - 1)

                idx = idx - 1
            elif curr_equation.equation[idx][0] in globals.leftUnOps:
                curr_equation.equation[idx][0] = calculate_unary(curr_equation.equation[idx - 1][0],
                                                                 curr_equation.equation[idx][0])
                eq_len -= 1

                # remove the operand used
                curr_equation.equation.pop(idx - 1)

                idx = idx - 1
        idx += 1

    # return the result contained in the last element of the equation list
    return curr_equation
