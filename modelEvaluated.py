# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 17:37:20 2020

@author: Asus
"""
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error
from math import sqrt, floor

#create and evaluate ARIMA model with parameters (p,d,q)

def modelEvaluated(data, sarimaOrder):
    #training data will be 8 years or 96 data points
    t = floor(len(data) * 0.8)
    x_train, x_test = data[0:t], data[t:]
    history = [x for x in x_train]
    #predictions
    predictions = list()
    order, sorder, trend = sarimaOrder
    for i in range(len(x_test)):
        model = SARIMAX(history, order=order, seasonal_order=sorder, trend=trend, simple_differencing=True, enforce_stationarity=False, enforce_invertibility=False)
        model_fit = model.fit(disp=False)
        y_hat = model_fit.forecast()[0]
        predictions.append(y_hat)
        history.append(x_test[i])
    #out-of-sample error
    error = mean_squared_error(x_test, predictions)
    return sqrt(error)