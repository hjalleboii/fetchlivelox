import requests
import json
import sys
import pgw
            

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


