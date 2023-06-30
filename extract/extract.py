import os
import requests
import bs4
import json
from commonExtract import config


class extractMainData:
    def __init__(self, *args):
        self.idx = None
        self.coordinates = [
            ["", ""],
            ["", ""],
            ["", ""],
            ["", ""],
        ]
        self.dataConfig = config()['config']['configurationObject']
        self.params = {
            'size': config()['config']['size_items'],
        }
        self.stateObject = []

    def createParamsObject(self, isInitialRequest:bool,coordinates, *cursor):
        obj = self.params.copy()
        obj.update({"latitude": coordinates[0], "longitude": coordinates[1]})
        if isInitialRequest == False:
            obj.update({
                'cursor': config()['config']['cursors'][cursor[0]],
                'section': config()['config']['section']
            })
        return obj

    def requestData(self):
        for i in range(38):
            pathFile = "./data/data{}.json".format(i)
            if os.path.exists(pathFile):
                continue
            for j in config()["config"]["cursors"]:
                params = self.createParamsObject(
                    True, self.coordinates[i]) if j == "cursor_0" else self.createParamsObject(False, self.coordinates[i], j)
                responseObj = requests.post(config()["config"]["URLRequest"], params=params, json=self.dataConfig)
                if responseObj.status_code == 200:
                    responseFiltered = responseObj.json()["sections"][0]["cards"]
                    for cardType in range(len(responseFiltered)):
                        if responseFiltered[cardType]["cardType"] == '':
                            responses = responseFiltered[cardType]["data"]["contents"]
                            [self.stateObject.append(response) for response in responses]
            if len(self.stateObject) > 0:
                f = open(pathFile, "x")
                f.write(json.dumps(self.stateObject,indent=4))
                f.close()
                self.stateObject.clear()


extractMainData().requestData()
