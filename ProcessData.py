# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 17:24:20 2020

@author: Asus
"""

import pandas as pd




def ProcessData(dictionary):
    df1 = pd.read_csv('DemandProcessed.csv', header=0, index_col=0)
#    demand = demand.T
    #getDict
    df2 = pd.DataFrame(dictionary, index=[len(df1)])
    demand = pd.concat([df1, df2], ignore_index=True)
    demand.to_csv('DemandProcessed.csv')
    dateRange = pd.date_range(start='1/1/2010', periods=len(demand), freq='M')
    demand.insert(loc=0, column='Date', value=dateRange)
    demand['DateStamp'] = pd.to_datetime(demand['Date'])
    demand = demand.set_index('DateStamp')
    demand.drop(['Date'], axis=1, inplace=True)
    return demand