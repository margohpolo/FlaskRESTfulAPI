# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 17:39:44 2020

@author: Asus
"""

from timeit import default_timer as timer
import bestModel
import pandas as pd



def GridSearchAndSave(data, params, columnName):
    Dict = {}
    start = timer()
    model = bestModel.bestModel(data, params)
    Dict[columnName] = model
    dt = timer() - start
    print("This took {0} mins".format(dt/60))
    return Dict