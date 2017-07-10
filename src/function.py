# -*- coding: utf-8 -*-
#

import pandas as pd
import numpy as np
import pickle

def ADD(A,B):
    return A+B

def LOG(A):
    pass

def REF(A,t):
    pass



def MINUS(A,B):
    return A-B

def MULTIPLY(A,B):
    return A*B

#return A/B
def DIVIDE(A,B):
    return A/B

#e.g. : A = [1,4,NaN] return [3,2,1]
def RANK(A):
    return A.rank(axis='columns', method='min', ascending=False)

#在从今天开始往前看t日，第几天是出现最大值的地方，今天是第t-1天，昨天是第t-2天
def TimeSeries_ArgMax(A,t):
    return A.rolling(t).apply(np.argmax)

def POWER(A,t):
    return A**t

def STD(A,t):
    return A.rolling(t).std()

def CORR(A,B,t):
    return A.rolling(t).corr(other = B)


#if t==0 return A
def DELTA(A,t):
    return A - A.shift(t)


def SUM(A,t):
    return A.rolling(t).sum()

def ABS(A):
    return abs(A)

def MEAN(A,t):
    return A.rolling(t).mean()


def IFbelow0(A, B, C):
    A1 = A.applymap(lambda x: 1 if x < 0 else 0)
    A2 = A.applymap(lambda x: 0 if x < 0 else 1)

    return A1 * B + A2 * C

def TimeSeries_MIN(A,t):
    return A.rolling(t).min()

def TimeSeries_MAX(A,t):
    return A.rolling(t).max()

#----------------------
def SIGN(A):
    return A.apply(np.sign)

def COV(A,B,t):
    return A.rolling(t).cov(other = B)










if __name__ == "__main__":
    with open('openPrice.pkl', 'rb') as file2:
        A = pickle.load(file2)

    with open('closePrice.pkl', 'rb') as file2:
        B = pickle.load(file2)

    C = COV(A,B,10)
    #C = TimeSeries_MIN(A,10)
    #D = MEAN(A,2)

    print C
    #print D