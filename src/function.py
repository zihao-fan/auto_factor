# -*- coding: utf-8 -*-
#

import pandas as pd
import numpy as np
import pickle
import datetime

def ADD(A,B):
    return A+B

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
    return A.rolling(int(t)).apply(np.argmax)

def POWER(A,t):
    return A**t

def STD(A,t):
    return A.rolling(int(t)).std()

def CORR(A,B,t):
    return A.rolling(int(t)).corr(other = B)


#if t==0 return A
def DELTA(A,t):
    return A - A.shift(int(t))


def SUM(A,t):
    return A.rolling(int(t)).sum()

def ABS(A):
    return abs(A)

def MEAN(A,t):
    return A.rolling(int(t)).mean()


def IFbelow0(A, B, C):
    A1 = A.applymap(lambda x: 1 if x < 0 else 0)
    A2 = A.applymap(lambda x: 0 if x < 0 else 1)

    return A1 * B + A2 * C

def TimeSeries_MIN(A,t):
    return A.rolling(int(t)).min()

def TimeSeries_MAX(A,t):
    return A.rolling(int(t)).max()

#----------------------
def SIGN(A):
    return A.apply(np.sign)

def COV(A,B,t):
    return A.rolling(int(t)).cov(other = B)


def LOG(A):
    return abs(A).applymap(np.log)

def REF(A,t):
    return A.shift(int(t))


#注：此函数执行耗时较长,约5s
def TimeSeries_RANK(A,t):
    return A.rolling(int(t)).apply(lambda x: x.argsort().argsort()[0])

def EMA(A,t):
    return A.ewm(span=t).mean()

def COUNT(A,t):
    pass

def AND(A,B):
    return (A.astype('bool')) & (B.astype('bool'))

def OR(A,B):
    return (A.astype('bool')) | (B.astype('bool'))


def MAX(A,B):
    C = A - B
    C1 = C.applymap(lambda x:0 if x < 0 else 1)
    C2 = C.applymap(lambda x: 1 if x < 0 else 0)
    return C1*A + C2*B

def MIN(A,B):
    C = A - B
    C1 = C.applymap(lambda x:1 if x < 0 else 0)
    C2 = C.applymap(lambda x: 0 if x < 0 else 1)
    return C1*A + C2*B

#A为bool类型的矩阵，如果真，选B，否则选C
def IF(A,B,C):
    A1 = A.astype('bool').astype('int')
    A2 = 1 - A1
    return A1*B + A2*C


def EQUAL(A,B):
    return (1-((A-B).astype('bool'))).astype('bool')

# 前面小于后面，返回TRUE
def LESS(A,B):
    C = A - B
    return C.applymap(lambda x:True if x<0 else False)

def AVEDEV(A,t):
    B = A.rolling(int(t)).mean()
    return ABS(A - B).rolling(int(t)).mean()


def SMA(A,t,k):
    return A.ewm(alpha=k/(t+1)).mean()

#A是逻辑运算矩阵，计算k个日期内有几个1
def COUNT(A,t):
    return A.astype('bool').astype('int').rolling(int(t)).sum()

def SQRT(A):
    return A.applymap(lambda x: 0 if x < 0 else np.sqrt(x))

def SCALE(A):
    return (A-A.mean())/A.std()

def DECAY_LINEAR(A,t):
    return A.rolling(int(t)).mean()





if __name__ == "__main__":
    with open('return.pkl', 'rb') as file2:
        A = pickle.load(file2)

    #with open('closePrice.pkl', 'rb') as file2:
    #    B = pickle.load(file2)

    #C = COV(A,B,10)
    #C = TimeSeries_MIN(A,10)
    #D = MEAN(A,2)

    #a = datetime.datetime.now()
    #C = SQRT(A)
    #b = datetime.datetime.now()

    C = SCALE(A)

    #print b-a
    #print A
    print C
    #print D