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
            

class Options:
    def __init__(self) -> None:
        self.worldfile = True
        self.savejson = False
        self.usejsonfile = False
        self.jsonfilepath = ""
        self.val =""
    def parse_arguments(self):
                
        arguments = sys.argv[1:]
        
        
        for i in range(0,len(arguments)):
            print(arguments[i])
            if i ==0:
                self.val = arguments[i]
            if arguments[i] == "--no-worldfile":
                self.worldfile = False
            if arguments[i] == "--save-worldfile":
                self.worldfile = False
            if arguments[i] == "-i" or arguments[i] == "--input":
                try:
                    self.val = arguments[i+1]
                except:
                    pass
            if arguments[i] == "--save-json":
                self.savejson = True
            if arguments[i] == "--no-json":
                self.savejson = False
            if arguments[i] == "--loadfromjson":
                try:
                    self.jsonfilepath = arguments[i+1]
                    self.usejsonfile = True

                except:
                    pass





def getfromclassstorageid(id):
    response = requests.get("https://livelox.blob.core.windows.net/class-storage/" +id)
    print(f"Request:  Status[{response.status_code}]  \"https://livelox.blob.core.windows.net/class-storage/{id}\"")
    if(response.status_code == 200):
        return response.text
    else:
        print("Request Failed")
        exit(1)
        
        


def downloadimage(url, name):
    response = requests.get(url)
    if(response.status_code == 200):
        with open(name,"wb") as image:
            image.write(response.content)


def GetContentsOfFile(name):
    with open(name,"rb") as file:
        return file.read()




def GetJsonData(options:Options):
    jsontext = ""
    if not options.usejsonfile:
        jsontext = getfromclassstorageid(options.val)
    else:
        jsontext = GetContentsOfFile(options.jsonfilepath)
    return json.loads(jsontext)


def main():

    options = Options()
    options.parse_arguments()
    
    jsondata = GetJsonData(options)
    name = jsondata["map"]["name"]
    
    if options.savejson:
        with open(options.val+".json","w") as file:
            file.write(json.dumps(options.jsondata,indent=4))
    if options.worldfile:
        pgw = PGW(jsondata)
        name += "_geo-" + pgw.type 
        pgw.write(name + ".pgw")

    
    downloadimage(jsondata["map"]["url"], name + ".png")

    

  


    

main()



