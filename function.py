# -*- coding: utf-8 -*-
#

import pandas as pd
import numpy as np
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

#在从今天开始往前看t日，第几天是出现最大值的地方，今天是第t-1天，昨天是第t-2天
def TimeSeries_ArgMax(A,t):
    return A.rolling(t).apply(np.argmax)

def POWER(A,t):
    pass

def STD(A,t):
    return A.rolling(t).std()

def CORR(A,B,t):
    pass

def DELTA(A,t):
    return A - A.rolling(t).apply(np.choose(0))

def SUM(A,t):
    return A.rolling(t).sum()

def ABS(A,t):
    pass

def MEAN(A,t):
    return A.rolling(t).mean()

def IF(A,B,C):
    pass

def TimeSeries_MIN(A,t):
    return A.rolling(t).min()

def TimeSeries_MAX(A,t):
    return A.rolling(t).max()

#----------------------
def SIGN(A):
    pass
    return A.sign()

def COV(A,B,t):
    pass










if __name__ == "__main__":
    with open('openPrice.pkl', 'rb') as file2:
        A = pickle.load(file2)

    with open('closePrice.pkl', 'rb') as file2:
        B = pickle.load(file2)

    C = DELTA(A,10)
    #C = TimeSeries_MIN(A,10)
    D = MEAN(A,2)

    print C
    #print D