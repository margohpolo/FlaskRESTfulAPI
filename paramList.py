# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 03:44:58 2020

@author: Asus
"""

def paramList(differenceCounter):
    params = list()
    p_values = range(2)
    d = differenceCounter
    q_values = range(2)
    P_values = range(2)
    D = differenceCounter
    Q_values = range(2)
    m = 12
    t = 'n'
    
    for p in p_values:
        for q in q_values:
            for P in P_values:
                for Q in Q_values:
                    param = [(p,d,q), (P,D,Q,m), t]
                    params.append(param)
    return params