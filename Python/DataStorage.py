import json
import datetime
import time

def addUser(name):
    with open("data\\users.json","r+") as json_file:
        data = json.load(json_file)
        new_user = {'name': name,
                    'score': 0
                    }
        data['users'].append(new_user)
        json_file.seek(0)
        json.dump(data,json_file,indent=4)
        json_file.truncate()



def getScore():
    jsonFile = open("data\\users.json","r+")
    data = json.load(jsonFile)
    output_string = "\n"
    for d in data['users']:
        output_string += d['name'] +': '+ str(d['score']) + '\n'
    return output_string

def addPoint(key):
    with open("data\\users.json","r+") as json_file:
        data = json.load(json_file)
        for d in data['users']:
            if key in d['name']: 
                test = d['score']
                test = test + 1
                d['score'] = test
        json_file.seek(0)
        json.dump(data,json_file,indent=4)
        json_file.truncate()
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
    
    return str(elapsed_time)
