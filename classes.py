# helper class to hold useful counters
class CounterHolder:
    def __init__(self):
        # counter for parentheses in the equation, keeps track of the priority
        # of the operators and checks for parentheses balance
        self.parentheses_multiplier = 0
        # counter for tilde operators in the equation, to make sure no multiple tilde operators are used
        self.tilde_cnt = 0
        # counter for minus operators in the equation
        self.minus_cnt = 0

    # increase priority of operators by 10 inside parentheses
    def inc_parentheses_multiplier(self):
        self.parentheses_multiplier += 10

    # decrease priority of operators by 10 after parentheses are closed
    def dec_parentheses_multiplier(self):
        self.parentheses_multiplier -= 10

    # return the value of the counter
    def get_parentheses_multiplier(self):
        return self.parentheses_multiplier

    # increase the value of the counter
    def inc_tilde_cnt(self):
        self.tilde_cnt += 1

    # returns the value of the counter
    def get_tilde_cnt(self):
        return self.tilde_cnt

    # reset the value of the counter
    def tilde_reset(self):
        self.tilde_cnt = 0

    # increase the minus counter
    def inc_minus_cnt(self):
        self.minus_cnt += 1

    # reset the minus counter
    def reset_minus_cnt(self):
        self.minus_cnt = 0

    # returns the value of the counter
    def get_minus_cnt(self):
        return self.minus_cnt


class OpString:
    """class used to store an operand before it is added to the new list"""
    def __init__(self, op_str):
        self.op_str = op_str

    def get_op_str(self):
        return self.op_str

    def add_to_op_str(self, string):
        self.op_str += string

    def add_to_beginning(self, string):
        self.op_str = string + self.op_str

    def empty_op_str(self):
        self.op_str = ''
