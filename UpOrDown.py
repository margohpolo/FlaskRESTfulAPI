# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 10:38:28 2020

@author: Asus
"""
import numpy as np


def UpOrDown(number):
    if number >= 0.00:
        number = np.ceil(number)
    elif number <= 0.00:
        number = np.floor(number)
    return number