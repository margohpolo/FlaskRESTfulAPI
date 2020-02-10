# -*- coding: utf-8 -*-

from statsmodels.tsa.stattools import adfuller

def adfuller_test(series, a, b, signif=0.05, name='', verbose=False,):
    """Perform ADFuller to test for Stationarity of given series and print report"""
    r = adfuller(series, autolag='AIC', regression='ct')
    output = {'test_statistic':round(r[0], 4), 'pvalue':round(r[1], 4), 'n_lags':round(r[2], 4), 'n_obs':r[3]}
    p_value = output['pvalue'] 
    def adjust(val, length= 6):
        return str(val).ljust(length)

    if p_value <= signif:
        a.append(name)
    else:
        b.append(name)