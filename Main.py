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

  def GenerateModel(dictionary, id):
    demand = ProcessData.ProcessData(dictionary)
    Prediction.GenerateModel(dictionary, demand)
    latestPrediction = Prediction.GetPrediction(dictionary, demand)
    loadDict[id] = latestPrediction
    with open("savedPredictions.txt", "a+") as outfile:
      json.dump({"id": id, "predictions": latestPrediction}, outfile)
      outfile.write("\n")
    print("latestPrediction type: ", type(latestPrediction), "\n latestPrediction: ", latestPrediction)
    return "Model Generation completed."

  def GetPrediction(dictionary):
    return Prediction.GetPrediction(dictionary)
  
  @app.route("/get")
  def get():
    get_id = request.args.get('id')
    found = False
    infile = open("savedPredictions.txt", "r")
    lines = infile.readlines()
    for line in lines:
      data = json.loads(line)
      if(data["id"] == get_id):
        found = True
        predictions = data["predictions"]
    if found:
      return {"predictions": predictions, "result": "success"}, 200
    else:
      return {"result": "failed"}, 200
#    return {get_id: (loadDict[get_id]).replace("\\","")}, 200 <- this is not working :()
  
api.add_resource(Main, '/<string:getDict_id>')


if __name__ == '__main__':
    app.run(debug=True, threaded=True)