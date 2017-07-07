# -*- coding: utf-8 -*-
import pandas as pd 
import function
import pickle
import os
from config import root_path

f = open('../data/openPrice.pkl', 'rb')
OPEN = pickle.load(f)
f = open('../data/closePrice.pkl', 'rb')
CLOSE = pickle.load(f)
t = 5

# add termial name for each data frame
terminal_set = {'OPEN', 'CLOSE', 'HIGH', 'LOW', 'VWAP', 'RETURNS', 'VOLUME', 't'}
# add key-value pair for each terminal
operands_dict = {'OPEN': OPEN,
                 'CLOSE': CLOSE,
                 't': t
}

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
        float(formula)
        is_digit = True
    except ValueError:
        is_digit = False
    if is_digit or formula in terminal_set:
        # print 'is terminal', formula
        return True
    # print 'not terminal', formula
    return False

def compute_node(data, isterminal):
    if isterminal:
        if data in operands_dict:
            return operands_dict[data]
        else:
            return float(data)
    else:
        slicing_point = find_slicing_point(data)
        current_operator = data[0:slicing_point[0]].strip()
        operands_list = []
        for i in range(len(slicing_point) - 1):
            operands_list.append(data[slicing_point[i]+1:slicing_point[i+1]].strip())
        results = []
        for substr in operands_list:
            results.append(compute_node(substr, is_terminal(substr)))
        # print 'Compute', current_operator
        return getattr(function, current_operator)(*results)

def compute_formula(formula, alpha_id):
    print '[Computing] alpha', alpha_id
    result = compute_node(formula[1:-1], is_terminal(formula[1:-1]))
    alpha_id = str(alpha_id)
    output_path = os.path.join(root_path, 'data', 'alpha' + alpha_id + '.pkl')
    result.to_pickle(output_path)
    print '[Done] alpha' + alpha_id, 'computed, output to', output_path

if __name__ == '__main__':
    compute_formula('(MULTIPLY(-1, CORR(RANK(OPEN), RANK(CLOSE), t)))', '001')