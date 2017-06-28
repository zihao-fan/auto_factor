# -*- coding: utf-8 -*-
#

import pandas as pd
import pickle

def ADD(A,B):
    return A+B

def MINUS(A,B):
    return A-B

def MULTIPLY(A,B):
    return A*B

#return A/B
def DEVIDE(A,B):
    return A/B

#e.g. : A = [1,4,NaN] return [3,2,1]
def RANK(A):
    return A.rank(axis='columns', method='min', ascending=False)

#在从今天开始往前看t日，第几天是出现最大值的地方，今天是第0天，昨天是第一天
def TimeSeries_ArgMax(A,t):
    pass

def POWER(A,t):
    pass

def STD(A,t):
    pass

def CORR(A,B,t):
    pass

def DELTA(A,t):
    pass

def SUM(A,t):
    pass

def ABS(A,t):
    pass

def MEAN(A):
    pass

def IF(A,B,C):
    pass

def TimeSeries_MIN(A,t):
    pass

def TimeSeries_MAX(A,t):
    pass

def SIGN(A):
    pass

def COV(A,B,t):
    pass










if __name__ == "__main__":
    with open('openPrice.pkl', 'rb') as file2:
        A = pickle.load(file2)

    with open('closePrice.pkl', 'rb') as file2:
        B = pickle.load(file2)

    C = RANK(A)

    print C