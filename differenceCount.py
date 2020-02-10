# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 17:33:52 2020

@author: Asus
"""

import adfuller_test

#Function to achieve Stationarity -> To count no. of Differences to do (variable d)


def differenceCount(df):
    allStationary = False
    #While loop counter
    c = 0
    #Counter for 0 columns
    n = 0
    #Count how many columns have 0 demand; to ignore their interfering with the ADF Test Loop
    for i in range(0, df.shape[1]):
        if (df.iloc[:,i].all() == 0):
            n += 1
    #While loop
    while allStationary == False:
        c += 1
        df = df.diff().dropna()
        a = []
        b = []
        # ADF Test on each column
        for name, column in df.iteritems():
            adfuller_test.adfuller_test(column, a, b, name=column.name)
        if len(b) == n:
            allStationary = True
    return c