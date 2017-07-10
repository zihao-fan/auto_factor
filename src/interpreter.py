# -*- coding: utf-8 -*-
import pandas as pd 
import function
import pickle
import os
import json
from config import root_path

def load_data(data_path):
    f = open(os.path.join(data_path, 'close.pkl'), 'rb')
    CLOSE = pickle.load(f)
    f = open(os.path.join(data_path, 'high.pkl'), 'rb')
    HIGH = pickle.load(f)
    f = open(os.path.join(data_path, 'low.pkl'), 'rb')
    LOW = pickle.load(f)
    f = open(os.path.join(data_path, 'marketValue.pkl'), 'rb')
    MKT_VALUE = pickle.load(f)
    f = open(os.path.join(data_path, 'open.pkl'), 'rb')
    OPEN = pickle.load(f)
    f = open(os.path.join(data_path, 'preClose.pkl'), 'rb')
    PRE_CLOSE = pickle.load(f)
    f = open(os.path.join(data_path, 'return.pkl'), 'rb')
    RETURNS = pickle.load(f)
    f = open(os.path.join(data_path, 'turnoverValue.pkl'), 'rb')
    TURN_OVER_VALUE = pickle.load(f)
    f = open(os.path.join(data_path, 'volume.pkl'), 'rb')
    VOLUME = pickle.load(f)
    f = open(os.path.join(data_path, 'vwap.pkl'), 'rb')
    VWAP = pickle.load(f)
    return OPEN, CLOSE, HIGH, LOW, MKT_VALUE, PRE_CLOSE, RETURNS, TURN_OVER_VALUE, VOLUME, VWAP

OPEN, CLOSE, HIGH, LOW, MKT_VALUE, PRE_CLOSE, RETURNS, TURN_OVER_VALUE, VOLUME, VWAP = load_data(os.path.join(root_path, 'data'))

# add termial name for each data frame
terminal_set = {'OPEN', 'CLOSE', 'HIGH', 'LOW', 'VWAP', 'RETURNS', 'VOLUME', 't', 'k'}
# add key-value pair for each terminal
operands_dict = {'OPEN': OPEN,
                 'CLOSE': CLOSE,
                 'HIGH': HIGH,
                 'LOW': LOW,
                 'VWAP': VWAP,
                 'RETURNS': RETURNS,
                 'VOLUME': VOLUME,
                 't': 5,
                 'k': 2
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

def compute_formula(alpha_id, formula):
    output_path = os.path.join(root_path, 'data', 'alpha' + alpha_id + '.pkl')
    if os.path.exists(output_path):
        print '[Skip]', alpha_id 'already exists.'
    else:   
        try:
            print '[Computing] alpha', alpha_id
            result = compute_node(formula[1:-1], is_terminal(formula[1:-1]))
            alpha_id = str(alpha_id)
            result.to_pickle(output_path)
            print '[Done] alpha' + alpha_id, 'computed, output to', output_path
        except e:
            print e
            print '[Exception]', alpha_id, 'fail to compute.'

def load_signal(file_path):
    with open(file_path, 'r') as f:
        signal_list = json.load(f)
        signal_list = [signal for signal in signal_list if signal[1] != 'pass']
        return signal_list

if __name__ == '__main__':
    # compute_formula('001', '(MULTIPLY(-1, CORR(RANK(OPEN), RANK(CLOSE), t)))')
    signal_list = load_signal(os.path.join(root_path, 'src', 'signal.json'))
    for signal in signal_list:
        compute_formula(signal[0], signal[1])