# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 17:20:46 2020

@author: Asus
"""
import ProcessData, paramList, differenceCount, GridSearchAndSave, UpOrDown
import warnings
from timeit import default_timer as timer

import pandas as pd
from multiprocessing import cpu_count
from joblib import Parallel, delayed, dump, load
from flask import json


import numpy as np



def GenerateModel(dictionary, demand):    
  warnings.filterwarnings("ignore")
  start = timer()
  print("Beginning process...")
#  demand = ProcessData.ProcessData(dictionary)
  #    print(demand.head())
  d = differenceCount.differenceCount(demand)
  print("differenceCount = ", d)
  #    j = 0
  params = list()
  modelsDict = {}
  
  demandDiff = demand
  
  for i in range(d):
      demandDiff = demandDiff.diff()
  
  #    print("Len of demandDiff: ", len(demandDiff))
  params = paramList.paramList(d)
  executor = Parallel(n_jobs=cpu_count(), backend='multiprocessing')
  tasks = (delayed(GridSearchAndSave.GridSearchAndSave)(pd.Series(columnData, name=columnName), params, columnName) for (columnName, columnData) in demandDiff.iteritems())
  modelsDict = executor(tasks)
  #    print("Dictionary of length ", len(modelsDict), "created.")
  
  try:
      dump(modelsDict, 'SARIMAS.joblib')
      print("modelsDict saved.")
  
  except:
      print("Unable to save models")
  #        continue
  dt = timer() - start
  print ("This took {0}hrs {1} mins".format((dt // 3600), ((dt / 3600)-(dt//3600))*60))
  
  
def GetPrediction(dictionary, demand):
  print("Loading models from saved .joblib file...")
  savedDict = load('SARIMAS.joblib')
  print("Generating predictions:")
  #    print(demand.head())
  d = differenceCount.differenceCount(demand)
  print("differenceCount = ", d)
  #    j = 0
  modelsDict = {}
  demandDiff = demand.diff()
  predDict = {}
  for item in savedDict:
      for key, value in item.items():
          predictions = value.fit().forecast(steps=1)
          print(predictions)
          predDict[key] = predictions #Next 2 months' predictions
   #Processing predDict, as predDict is currently a tuple followed by float
  list1 = []
  list2 = []
  list3 = []
  list4 = []
  list5 = []
  
  print("predDict: \n", predDict)
#  Math needs fixing (I think); don't know why suddenly stopped working
  for (key,value) in predDict.items():
      list1.append(key)
      list2.append(predDict[key])
  print("List2:\n", list2)
  for item in list2:
      for (x,y) in np.ndenumerate(item):
        list3.append(UpOrDown.UpOrDown(y))
  print("List3:\n", list3)
  for i in range(len(demand.columns)):
    list5.append(demand[list1[i]].iloc[-1])
  
  print("List5:\n", list5)
    
  
  for j in range(0,len(demand.columns)):
    list4.append(list3[j] + list5[j])
    
  
  for m in range(len(demand.columns)):
    predDict[list1[m]] = list4[m]
      
  print("List4:\n", list4)
  print("Length of predDict: ", len(predDict))
  print("predDict after: ", predDict)
  #Dump predDict as a JSON string
  dictDump = json.dumps(predDict)
  
  print("dictDump type: ", type(dictDump), "\n", "dictDump:\n", dictDump)
  
  return dictDump
