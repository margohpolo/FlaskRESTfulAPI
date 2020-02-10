# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 17:38:18 2020

@author: Asus
"""

import modelEvaluated, paramList
from statsmodels.tsa.statespace.sarimax import SARIMAX
from math import floor

#evaluate possible combos of (p,d,q) for best-performing model

def bestModel(data, params):
    data = data.astype('float32')
    
    best_score, best_para = float("inf"), None
    for param in params:
        sarimaOrder = param
        try:
           rmse = modelEvaluated.modelEvaluated(data, sarimaOrder)
           if rmse < best_score:
               best_score, best_para = rmse, sarimaOrder
               print("SARIMA{0} RMSE={1}".format(sarimaOrder, rmse))
        except:
            print("This one failed - ", sarimaOrder, "...moving on...")
            continue
    print("\nBEST SARIMA{0} RMSE={1}".format(best_para, best_score))
#     (p, d, q) = np.vectorize(best_score, signature="(m)->()")
#     (p, d, q) = [(a, b, c) for item in zip(best_score)]
#     print(best_score, type(best_score))
    
    t = floor(len(data) * 0.8)
    history = [x for x in data[0:t]]
    order, sorder, trend = best_para
    modelBest = SARIMAX(history, order=order, seasonal_order=sorder, trend=trend, simple_differencing=True, enforce_stationarity=False, enforce_invertibility=False)
#     modelBest_fit = modelBest.fit(disp=0)
    return modelBest