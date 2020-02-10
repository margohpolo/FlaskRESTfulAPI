# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 13:31:02 2020

@author: Maaaaarrrkkk
"""

import Prediction

from flask import Flask, request, json
from flask_restful import Resource, Api
from datetime import datetime


app = Flask(__name__)
api = Api(app)

getDict = {}
loadDict = {}
latestPrediction = ""

class Main(Resource):
  now = datetime.now()
  getDict_id = now.strftime("%dd%mm%YY")

#    def appendToDF(dictionary):
      # MUST add demand to this file 1st
      # for columnName, columnData in demand.iteritems():
          # for (x, y) in dictionary[columnName]:
              # demand[columnName].append(x)
              # demand[columnName].append(y)
      # After this step then do Differencing

  def put(self, getDict_id):
    getDict[getDict_id] = request.form['data']
    loadDict = json.loads(getDict[getDict_id].replace('\'', '\"'))
    latestPrediction = Main.MakePrediction(loadDict)
    return {getDict_id: latestPrediction}, 200
#    return {getDict_id: getDict[getDict_id]}

  def MakePrediction(dictionary):
    return Prediction.Prediction(dictionary)
  
  def get(self, getDict_id):
    return {latestPrediction}, 200
  
api.add_resource(Main, '/<string:getDict_id>')


if __name__ == '__main__':
    app.run(debug=True)