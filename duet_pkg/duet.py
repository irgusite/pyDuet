import requests
import json

class duet:
    duetStatusJson = None
    duetOnline = False
    def __init__(self, host, password = None):
        self.host = host
        self.password = password

    def getStatusUpdate(self):
        try:
            req = requests.get(self.host+"/rr_status?type=2", timeout=2)
            j = json.loads(req.text)
            self.duetStatusJson = j
            self.duetOnline = True
        except requests.Timeout as e:
            self.duetOnline = False
        print("Duet3D is online: "+str(self.duetOnline))

    def getDuetStatus(self):
        """Returns the status code of the printer/CNC."""
        return self.duetStatusJson["status"]

    def getDuetStatusFull(self):
        """Returns the human readable status code of the printer/CNC."""
        switcher={
            "I":"Idle",
            "P":"Printing",
            "C":"Configuration file processing",
            "B":"Busy",
            "D":"Decelerating",
            "S":"Stopped",
            "R":"Resuming",
            "H":"Halted",
            "F":"Flashing firmware",
            "T":"Tool changing"
        }
        return switcher.get(self.duetStatusJson["status"], None)

    def getHomedAxis(self):
        """ Returns the homing state of the axis as an array of 3 axis.
        """
        
        return self.duetStatusJson["coords"]["axesHomed"]

    def getHeadPosition(self):
        """ Returns the xyz coordinates of the toolhead
        """
        return self.duetStatusJson["coords"]["xyz"]

    def getTemps(self):
        temps = self.duetStatusJson["temps"]["current"]
        print(len(temps))

    def getNbTools(self):
        return int(len(self.duetStatusJson["tools"]))

    def getLoadedFilament(self, tool):
        return self.duetStatusJson["tools"][tool]["filament"]



        

d = duet("http://192.168.1.41")
d.getStatusUpdate()
print(d.getLoadedFilament(1))
