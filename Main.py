# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 13:31:02 2020

@author: Maaaaarrrkkk
"""

import Prediction, threading, ProcessData

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

  @app.route("/put", methods=["PUT"])
  def put():
    getDict_id = request.args.get('id')
    getDict[getDict_id] = request.args.get('data')
    loadDict = json.loads(getDict[getDict_id].replace('\'', '\"'))
    thread = threading.Thread(target=Main.GenerateModel, args=(loadDict, getDict_id))
    thread.daemon = True
    thread.start()
    #latestPrediction = Main.MakePrediction(loadDict)
    #return {getDict_id: latestPrediction}, 200
    return "Put completed."

  def GenerateModel(dictionary, id):
    demand = ProcessData.ProcessData(dictionary)
    Prediction.GenerateModel(dictionary, demand)
    latestPrediction = Prediction.GetPrediction(dictionary, demand)
    loadDict[id] = latestPrediction
    print("latestPrediction type: ", type(latestPrediction), "\n latestPrediction: ", latestPrediction)
    return "Model Generation completed."

#  def GetPrediction(dictionary, id):
#    loadDict_id = id
#    latestPrediction = Prediction.GetPrediction(dictionary)    
#    print("latestPrediction type: ", type(latestPrediction), "\n latestPrediction: ", latestPrediction)
#
#    return latestPrediction
  
  @app.route("/get", methods=["GET"])
  def get():
    get_id = request.args.get('id')
#    dictionary = request.args.get('data')
#    loadDict = json.loads(dictionary.replace('\'', '\"'))
    return {get_id: loadDict[get_id]}, 200
    #return {latestPrediction}, 200
  
api.add_resource(Main, '/<string:getDict_id>')


if __name__ == '__main__':
    app.run(debug=True, threaded=True)