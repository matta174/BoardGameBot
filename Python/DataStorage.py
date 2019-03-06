import json


def getData():
    jsonFile = open("data\\users.json","r+")
    data = json.load(jsonFile)
    return data
