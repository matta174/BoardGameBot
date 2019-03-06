import json
import datetime
import time

def getData():
    jsonFile = open("data\\users.json","r+")
    data = json.load(jsonFile)
    return data

def getStartTime():
    jsonFile = open("data\\playtime.json","r+")
    data = json.load(jsonFile)
    return data["start time"]

def setStartTime():
    start_time = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
    with open("data\\playtime.json","r+") as json_file:
        json_decoded = json.load(json_file)
    json_decoded["start time"] = start_time
    with open("data\\playtime.json","r+") as json_file:
        json.dump(json_decoded, json_file)

def getEndTime():
    jsonFile = open("data\\playtime.json","r+")
    data = json.load(jsonFile)
    string_date = data["start time"]
    formatted_datetime_object = datetime.datetime.strptime(string_date,'%Y-%m-%dT%H:%M:%S.%f')
    elapsed_time = datetime.datetime.now() - formatted_datetime_object 
    stringtime = str(elapsed_time)
    return str(stringtime)
