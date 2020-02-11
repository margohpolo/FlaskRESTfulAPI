# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 13:31:02 2020

@author: Maaaaarrrkkk
"""

import Prediction
import threading
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

  @app.route("/put")
  def put():
    getDict_id = request.args.get('id')
    getDict[getDict_id] = request.args.get('data')
    loadDict = json.loads(getDict[getDict_id].replace('\'', '\"'))
    thread = threading.Thread(target=Main.GenerateModel, args=(loadDict,))
    thread.daemon = True
    thread.start()
    #latestPrediction = Main.MakePrediction(loadDict)
    #return {getDict_id: latestPrediction}, 200
    return "hello"

  def GenerateModel(dictionary):
    return Prediction.GenerateModel(dictionary)

  def GetPrediction(dictionary):
    return Prediction.GetPrediction(dictionary)
  
  @app.route("/get")
  def get():
    getDict_id = request.args.get('id')
    dictionary = request.args.get('data')
    loadDict = json.loads(dictionary.replace('\'', '\"'))
    return {getDict_id: Main.GetPrediction(loadDict)}, 200
    #return {latestPrediction}, 200
  
api.add_resource(Main, '/<string:getDict_id>')


if __name__ == '__main__':
    app.run(debug=True, threaded=True)