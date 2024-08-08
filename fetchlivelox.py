import requests
import json
import sys
class PGW:
    
    
    
    
    
    
    def __init__(self,jsondata):
        

        pos = [[0, 0] for _ in range(4)]
        if "projectedBoundingQuadrilateral" in jsondata["map"]:
            for i in range(4):
                pos[i][0] = jsondata["map"]["projectedBoundingQuadrilateral"]["vertices"][i]["x"]
                pos[i][1] = jsondata["map"]["projectedBoundingQuadrilateral"]["vertices"][i]["y"]
                self.type = str( jsondata["map"]["projectionEpsgCode"] )
        else:
            for i in range(4):
                pos[i][0] = jsondata["map"]["boundingQuadrilateral"]["vertices"][i]["longitude"]
                pos[i][1] = jsondata["map"]["boundingQuadrilateral"]["vertices"][i]["latitude"]
                self.type = "GPS"
       

        width = jsondata["map"]["width"]
        height = jsondata["map"]["height"]

        self.a = (pos[2][0] - pos[3][0])/float(width)
        self.d = (pos[2][1] - pos[3][1])/float(width)


        self.b = (pos[0][0] - pos[3][0])/float(height)
        self.e = (pos[0][1] - pos[3][1])/float(height)



        self.c = pos[3][0]   
        self.f = pos[3][1]        
        




    def write(self,file):
        with open(file,"w") as file:
            file.write(format(self.a, '.15f') + "\n" + format(self.d, '.15f') + "\n" + format(self.b, '.15f') + "\n" + format(self.e, '.15f') + "\n" + format(self.c, '.15f') + "\n" + format(self.f, '.15f') + "\n")
            
            

def getfromclassstorageid(id):
    response = requests.get("https://livelox.blob.core.windows.net/class-storage/" +id)

    if(response.status_code == 200):
        return response.text
    else:
        return "{}"


def downloadimage(url, name):
    response = requests.get(url)
    if(response.status_code == 200):
        with open(name,"wb") as image:
            image.write(response.content)


def GetContentsOfFile(name):
    with open(name,"rb") as file:
        return file.read()

arguments = sys.argv[1:]



#val = "0000735681_3921540601865" # norrskogslången
val = "0000655309_3921029604560" # USM karlskrona 23
#val = "0000640214_3921130392297" # col de hares : frankrike
#val = "0000729477_3921811132242" # tranan klubbträning

worldfile = True
savejson = False
usejsonfile = False
jsonfilepath = ""
for i in range(0,len(arguments)):
    if i ==0:
        val = arguments[i]
    if arguments[i] == "--no-worldfile":
        worldfile = False
    if arguments[i] == "--save-worldfile":
        worldfile = False
    if arguments[i] == "-i" or arguments[i] == "--input":
        try:
            val = arguments[i+1]
        except:
            pass
    if arguments[i] == "--save-json":
        savejson = True
    if arguments[i] == "--no-json":
        savejson = False
    if arguments[i] == "--loadfromjson":
        try:
            usejsonfile = True
            jsonfilepath = arguments[i+1]
        except:
            pass


jsontext = ""
if not usejsonfile:
    jsontext = getfromclassstorageid(val)
else:
    jsontext = GetContentsOfFile(jsonfilepath)
jsondata = json.loads(jsontext)


if savejson:
    with open(val+".json","w") as file:
        file.write(json.dumps(jsondata,indent=4))

name = jsondata["map"]["name"]

if worldfile:
    pgw = PGW(jsondata)
    name += " geo-" + pgw.type
    pgw.write(name +".pgw")



downloadimage(jsondata["map"]["url"], name + ".png")


