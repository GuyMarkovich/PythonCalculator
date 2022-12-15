from input_handler import *


# testing simple syntax errors
def test_syntax_error():
    assert calculate_equation('1 + 2 +') == 'Error'
    assert calculate_equation('!4') == 'Error'
    assert calculate_equation('7+*4') == 'Error'
    assert calculate_equation('7-~~5') == 'Error'
    assert calculate_equation('7^+5') == 'Error'


# test equation with completely invalid syntax (not even a number)
def test_invalid_syntax():
    assert calculate_equation('abecj') == 'Error'


# test empty equation
def test_empty_equation():
    assert calculate_equation('') == 0


# test equation with only whitespace
def test_only_whitespace():
    assert calculate_equation('   ') == 0


# test individual operators with numbers
def test_individual_operators():
    assert calculate_equation('1+2') == 3.0
    assert calculate_equation('1-2') == -1.0
    assert calculate_equation('1*2') == 2.0
    assert calculate_equation('1/2') == 0.5
    assert calculate_equation('1^2') == 1.0
    assert calculate_equation('1%2') == 1.0
    assert calculate_equation('1$2') == 2.0
    assert calculate_equation('1&2') == 1.0
    assert calculate_equation('1@2') == 1.5
    assert calculate_equation('~2') == -2.0
    assert calculate_equation('2!') == 2.0
    assert calculate_equation('24#') == 6.0


# test operators with invalid syntax
def test_invalid_operators():
    assert calculate_equation('-2!') == 'Error'
    assert calculate_equation('~~4') == 'Error'
    assert calculate_equation('-(4!)!') == 'Error'
    assert calculate_equation('-3^-2.5') == 'Error'
    assert calculate_equation('-~5!') == 'Error'
    assert calculate_equation('_5') == 'Error' # use of an internal operator by the user


# test complex equations
def test_complex_equations():
    assert calculate_equation('-(6!*6+(5--4))&(4+3*7^6)') == -4329.
    assert calculate_equation('56478389# - 67&89*0.5') == 16.5
    assert calculate_equation('897%23 * 2^7 /(4*7$9)') == 0.0
    assert calculate_equation('1.38^2.5 * 7^9# - 4.5') == 90277610.28940076
    assert calculate_equation('56&78$93 * 787# - (57!+4.5)') == -4.052691950487722e+76
    assert calculate_equation('-(5!+4.5) - ~ (90^2 - 67!)') == -3.647111091818868e+94
    assert calculate_equation('-~(90-5) - 5! + 456## *2') == -23.0
