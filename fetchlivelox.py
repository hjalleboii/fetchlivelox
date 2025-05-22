#!/usr/bin/env python3
import requests
import argparse
import json
import sys

from urllib.parse import urlparse, parse_qs



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
            


def parseargs():
    parser = argparse.ArgumentParser(description="Downloads Maps from livelox.com")
    parser.add_argument("urlorclassid",help="url to livelox event or classId")
    parser.add_argument("-N","--name",type=str, required = False,help="Name of the map, defaults to the name provided by livelox",default="")

    return parser.parse_args()

args = parseargs()
class_id = 0
try:
    class_id = int(args.urlorclassid)
except:
    query = urlparse(args.urlorclassid).query
    params = parse_qs(query)
    class_id = params.get('classId', [None])[0]

session = requests.Session()

session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "en",
    "Connection": "keep-alive",
})

ajax_headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Content-Type": "application/json",
    "Origin": "https://www.livelox.com",
    "X-Requested-With": "XMLHttpRequest"
}

r2 = session.post("https://www.livelox.com/Data/ClassBlob",json={"classIds":[class_id],"includeMap":True},headers=ajax_headers)

jsondata = r2.json()


pgw = PGW(jsondata)

name = (jsondata["map"]["name"] if args.name == "" else args.name) +"_"+pgw.type

image_map = session.get(jsondata["map"]["url"]).content
with open(name+".png","wb") as image:
    image.write(image_map)
pgw.write(name+".pgw")
