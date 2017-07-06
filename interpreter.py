# -*- coding: utf-8 -*-
import pandas as pd 
import function
import pickle

f = open('openPrice.pkl', 'rb')
OPEN = pickle.load(f)
f = open('closePrice.pkl', 'rb')
CLOSE = pickle.load(f)

terminal_dict = {'OPEN', 'VOLUME', 'CLOSE', 'VWAP', 't'}
function_dict = {'MULTIPLY'}
operands_dict = {'OPEN': OPEN,
                 'CLOSE': CLOSE
}

class Node(object):
    def __init__(self, data, is_terminal):
        self.data = data
        self.is_terminal = is_terminal

def find_slicing_point(formula):
    length = len(formula)
    left_parenth_idx = 0
    right_parenth_idx = 0
    for i in range(length):
        if formula[i] == '(':
            left_parenth_idx = i
            break
    for i in range(length):
        if formula[length - 1 - i] == ')':
            right_parenth_idx = length - 1 - i
            break
    depth = 0
    comma_list = []
    for i in range(length):
        if formula[i] == '(':
            depth += 1
        if formula[i] == ')':
            depth -=1
        if depth == 1 and formula[i] == ',':
            comma_list.append(i)
    return [left_parenth_idx] + comma_list + [right_parenth_idx]

def is_terminal(formula):
    is_digit = False
    try:
        int(formula)
        is_digit = True
    except ValueError:
        is_digit = False
    if is_digit or formula in terminal_dict:
        print 'is terminal', formula
        return True
    print 'not terminal', formula
    return False

def compute_node(node):
    if node.is_terminal:
        if node.data in operands_dict:
            return operands_dict[node.data]
        else:
            return int(node.data)
    else:
        slicing_point = find_slicing_point(node.data)
        current_operator = node.data[0:slicing_point[0]].strip()
        operands_list = []
        for i in range(len(slicing_point) - 1):
            operands_list.append(node.data[slicing_point[i]+1:slicing_point[i+1]].strip())
        results = []
        for substr in operands_list:
            results.append(compute_node(Node(substr, is_terminal(substr))))
        print 'Compute', current_operator
        return getattr(function, current_operator)(*results)

def compute_formula(formula):
    root_node = Node(formula[1:-1], is_terminal(formula[1:-1]))
    compute_node(root_node)

if __name__ == '__main__':
    compute_formula('(MULTIPLY(-1, CORR(RANK(OPEN), RANK(CLOSE), 5)))')
