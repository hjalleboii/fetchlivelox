#!/usr/bin/env python3
import requests
import argparse
import json
import sys

import numpy as np
import drawsvg
import math
from PIL import Image
import io
import cairosvg
import time
from urllib.parse import urlparse, parse_qs


session = requests.Session()

session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "en",
    "Connection": "keep-alive",
})

svg_numbers = [
    (0.6379585326953748,"M0.000,0.501 C0.000,0.384 0.011,0.292 0.035,0.222 C0.059,0.150 0.094,0.096 0.142,0.057 C0.188,0.019 0.247,0.000 0.319,0.000 C0.372,0.000 0.418,0.011 0.458,0.032 C0.496,0.053 0.530,0.085 0.555,0.124 C0.581,0.164 0.601,0.212 0.616,0.270 C0.630,0.327 0.638,0.404 0.638,0.501 C0.638,0.616 0.627,0.708 0.603,0.778 C0.579,0.848 0.544,0.904 0.496,0.943 C0.450,0.981 0.391,1.000 0.319,1.000 C0.225,1.000 0.150,0.967 0.097,0.898 C0.032,0.817 0.000,0.684 0.000,0.501 L0.000,0.501 M0.123,0.501 C0.123,0.662 0.142,0.769 0.180,0.821 C0.217,0.874 0.263,0.901 0.319,0.901 C0.375,0.901 0.421,0.874 0.458,0.821 C0.496,0.767 0.515,0.660 0.515,0.501 C0.515,0.340 0.496,0.233 0.458,0.180 C0.421,0.126 0.373,0.100 0.317,0.100 C0.262,0.100 0.219,0.123 0.185,0.171 C0.144,0.230 0.123,0.340 0.123,0.501"),
    (0.36044657097288535,"M0.360,1.000 0.241,1.000  0.241,0.234  C0.211,0.263 0.174,0.290 0.126,0.317 C0.080,0.346 0.037,0.367 0.000,0.380 L0.000,0.263  C0.067,0.233 0.126,0.195 0.175,0.148 C0.226,0.104 0.262,0.061 0.282,0.018 L0.360,0.018"),
    (0.6475279106858058,"M0.648,0.885 0.648,1.000  0.000,1.000  C0.000,0.971 0.005,0.944 0.014,0.917 C0.032,0.874 0.057,0.829 0.094,0.788 C0.131,0.745 0.182,0.695 0.250,0.640 C0.357,0.552 0.429,0.483 0.467,0.432 C0.504,0.381 0.523,0.333 0.523,0.287 C0.523,0.239 0.506,0.199 0.472,0.166 C0.437,0.134 0.394,0.118 0.338,0.118 C0.281,0.118 0.234,0.136 0.199,0.169 C0.164,0.204 0.147,0.252 0.147,0.314 L0.024,0.301  C0.032,0.209 0.064,0.139 0.120,0.091 C0.174,0.041 0.249,0.018 0.341,0.018 C0.435,0.018 0.509,0.045 0.565,0.096 C0.619,0.148 0.646,0.212 0.646,0.290 C0.646,0.329 0.638,0.367 0.622,0.405 C0.606,0.443 0.579,0.483 0.542,0.525 C0.506,0.566 0.443,0.624 0.357,0.697 C0.285,0.758 0.239,0.799 0.219,0.820 C0.198,0.842 0.180,0.863 0.167,0.885"),
    (0.6411483253588534,"M0.000,0.726 0.121,0.708  C0.134,0.777 0.158,0.826 0.191,0.856 C0.225,0.887 0.265,0.901 0.313,0.901 C0.368,0.901 0.416,0.882 0.456,0.842 C0.494,0.804 0.514,0.754 0.514,0.697 C0.514,0.641 0.496,0.596 0.459,0.560 C0.424,0.525 0.378,0.507 0.322,0.507 C0.300,0.507 0.271,0.510 0.238,0.520 L0.250,0.415  C0.258,0.415 0.266,0.416 0.271,0.416 C0.322,0.416 0.368,0.402 0.408,0.376 C0.450,0.349 0.470,0.308 0.470,0.252 C0.470,0.209 0.455,0.172 0.426,0.144 C0.396,0.113 0.357,0.099 0.309,0.099 C0.263,0.099 0.225,0.115 0.193,0.144 C0.163,0.172 0.142,0.217 0.132,0.276 L0.013,0.254  C0.027,0.174 0.061,0.112 0.113,0.067 C0.164,0.022 0.230,0.000 0.308,0.000 C0.360,0.000 0.410,0.013 0.455,0.035 C0.499,0.057 0.534,0.089 0.558,0.129 C0.582,0.169 0.593,0.211 0.593,0.255 C0.593,0.297 0.582,0.335 0.560,0.370 C0.537,0.405 0.504,0.432 0.459,0.453 C0.517,0.467 0.561,0.494 0.593,0.536 C0.625,0.579 0.641,0.632 0.641,0.694 C0.641,0.780 0.611,0.852 0.549,0.912 C0.486,0.971 0.407,1.000 0.313,1.000 C0.226,1.000 0.155,0.974 0.097,0.923 C0.041,0.872 0.010,0.807 0.000,0.726"),
    (0.6778309409888358,"M0.426,1.000 0.426,0.767  0.000,0.767  0.000,0.657  0.447,0.022  0.545,0.022  0.545,0.657  0.678,0.657  0.678,0.767  0.545,0.767  0.545,1.000  L0.426,1.000 M0.426,0.657 0.426,0.215  0.118,0.657"),
    (0.6491228070175428,"M0.000,0.727 0.126,0.716  C0.136,0.778 0.158,0.825 0.191,0.855 C0.225,0.885 0.266,0.901 0.314,0.901 C0.373,0.901 0.421,0.879 0.461,0.836 C0.501,0.793 0.522,0.734 0.522,0.662 C0.522,0.593 0.502,0.539 0.464,0.499 C0.426,0.461 0.375,0.440 0.313,0.440 C0.274,0.440 0.239,0.450 0.207,0.467 C0.177,0.485 0.152,0.507 0.134,0.536 L0.021,0.520  0.116,0.018  0.603,0.018  0.603,0.132  0.212,0.132  0.159,0.396  C0.219,0.354 0.281,0.335 0.344,0.335 C0.431,0.335 0.502,0.364 0.561,0.423 C0.620,0.482 0.649,0.558 0.649,0.651 C0.649,0.740 0.624,0.817 0.571,0.880 C0.509,0.960 0.423,1.000 0.314,1.000 C0.225,1.000 0.153,0.974 0.097,0.925 C0.040,0.876 0.008,0.809 0.000,0.727"),
    (0.6459330143540644,"M0.628,0.244 0.509,0.254  C0.498,0.206 0.483,0.172 0.464,0.152 C0.431,0.116 0.391,0.099 0.343,0.099 C0.305,0.099 0.271,0.110 0.242,0.131 C0.204,0.159 0.175,0.199 0.153,0.252 C0.131,0.305 0.120,0.381 0.120,0.478 C0.148,0.434 0.183,0.402 0.225,0.381 C0.266,0.359 0.311,0.348 0.357,0.348 C0.437,0.348 0.506,0.378 0.561,0.437 C0.617,0.496 0.646,0.573 0.646,0.665 C0.646,0.727 0.633,0.785 0.606,0.837 C0.579,0.890 0.544,0.930 0.498,0.959 C0.451,0.986 0.399,1.000 0.340,1.000 C0.239,1.000 0.158,0.963 0.094,0.890 C0.032,0.817 0.000,0.694 0.000,0.525 C0.000,0.337 0.035,0.199 0.104,0.113 C0.166,0.038 0.247,0.000 0.351,0.000 C0.427,0.000 0.491,0.022 0.541,0.065 C0.589,0.108 0.619,0.167 0.628,0.244 L0.628,0.244 M0.137,0.667 C0.137,0.708 0.147,0.746 0.164,0.785 C0.182,0.823 0.206,0.852 0.238,0.871 C0.270,0.892 0.303,0.901 0.338,0.901 C0.388,0.901 0.432,0.880 0.469,0.841 C0.504,0.799 0.523,0.743 0.523,0.673 C0.523,0.604 0.506,0.552 0.469,0.514 C0.432,0.474 0.388,0.455 0.333,0.455 C0.279,0.455 0.233,0.474 0.195,0.514 C0.156,0.552 0.137,0.603 0.137,0.667"),
    (0.6331738437001594,"M0.000,0.150 0.000,0.035  0.633,0.035  0.633,0.128  C0.571,0.195 0.510,0.282 0.448,0.392 C0.388,0.502 0.340,0.616 0.306,0.732 C0.282,0.813 0.268,0.903 0.260,1.000 L0.137,1.000  C0.139,0.923 0.153,0.831 0.182,0.722 C0.212,0.612 0.254,0.507 0.306,0.407 C0.360,0.305 0.418,0.220 0.480,0.150"),
    (0.6459330143540644,"M0.187,0.453 C0.137,0.434 0.100,0.408 0.077,0.375 C0.051,0.341 0.040,0.300 0.040,0.254 C0.040,0.182 0.065,0.121 0.116,0.073 C0.167,0.026 0.236,-0.000 0.321,-0.000 C0.407,-0.000 0.475,0.026 0.528,0.075 C0.579,0.124 0.604,0.185 0.604,0.257 C0.604,0.301 0.593,0.341 0.569,0.375 C0.545,0.408 0.509,0.434 0.461,0.453 C0.522,0.472 0.566,0.504 0.598,0.547 C0.630,0.592 0.646,0.643 0.646,0.703 C0.646,0.788 0.616,0.858 0.557,0.914 C0.498,0.971 0.419,1.000 0.322,1.000 C0.226,1.000 0.148,0.971 0.089,0.914 C0.030,0.856 0.000,0.786 0.000,0.700 C0.000,0.636 0.016,0.584 0.049,0.541 C0.081,0.498 0.128,0.467 0.187,0.453 L0.187,0.453 M0.163,0.249 C0.163,0.295 0.177,0.333 0.207,0.362 C0.238,0.392 0.276,0.407 0.324,0.407 C0.370,0.407 0.408,0.392 0.437,0.362 C0.467,0.333 0.482,0.298 0.482,0.255 C0.482,0.212 0.466,0.174 0.435,0.145 C0.405,0.115 0.367,0.099 0.322,0.099 C0.276,0.099 0.238,0.115 0.207,0.144 C0.177,0.172 0.163,0.207 0.163,0.249 L0.163,0.249 M0.124,0.700 C0.124,0.735 0.132,0.769 0.148,0.801 C0.164,0.833 0.188,0.856 0.220,0.874 C0.252,0.893 0.287,0.901 0.324,0.901 C0.381,0.901 0.429,0.882 0.466,0.845 C0.504,0.809 0.523,0.762 0.523,0.705 C0.523,0.648 0.504,0.600 0.464,0.561 C0.426,0.523 0.378,0.504 0.321,0.504 C0.263,0.504 0.217,0.523 0.180,0.561 C0.142,0.598 0.124,0.644 0.124,0.700"),
    (0.6443381180223273,"M0.018,0.758 0.134,0.746  C0.144,0.801 0.163,0.841 0.190,0.864 C0.217,0.888 0.252,0.901 0.297,0.901 C0.333,0.901 0.365,0.893 0.392,0.876 C0.421,0.860 0.443,0.836 0.461,0.809 C0.478,0.780 0.494,0.742 0.506,0.694 C0.518,0.646 0.525,0.596 0.525,0.547 C0.525,0.541 0.525,0.533 0.523,0.523 C0.499,0.561 0.467,0.592 0.426,0.616 C0.383,0.640 0.338,0.651 0.290,0.651 C0.209,0.651 0.140,0.622 0.085,0.563 C0.029,0.504 0.000,0.427 0.000,0.332 C0.000,0.231 0.029,0.152 0.088,0.091 C0.147,0.030 0.220,-0.000 0.308,-0.000 C0.372,-0.000 0.429,0.018 0.483,0.053 C0.536,0.086 0.576,0.136 0.603,0.198 C0.630,0.262 0.644,0.354 0.644,0.474 C0.644,0.600 0.630,0.699 0.603,0.772 C0.576,0.847 0.536,0.903 0.482,0.943 C0.427,0.981 0.365,1.000 0.293,1.000 C0.217,1.000 0.155,0.979 0.105,0.936 C0.057,0.893 0.029,0.834 0.018,0.758 L0.018,0.758 M0.510,0.325 C0.510,0.257 0.491,0.201 0.455,0.161 C0.418,0.120 0.375,0.100 0.322,0.100 C0.270,0.100 0.223,0.121 0.183,0.166 C0.144,0.209 0.124,0.266 0.124,0.335 C0.124,0.397 0.142,0.448 0.180,0.486 C0.217,0.526 0.265,0.545 0.319,0.545 C0.375,0.545 0.421,0.526 0.456,0.486 C0.493,0.448 0.510,0.394 0.510,0.325")
]
coursePrintColor = "#A626FF"
default_controlConnectionLineWidth = 5.2

default_start_symbolSize = 300
default_control_symbolSize = 45
default_finish_symbolSize = 52.5
default_symbolSize = [
    default_start_symbolSize,
    default_control_symbolSize,
    default_finish_symbolSize    
]
default_symbolLineWidth = 5.2


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
            

def get_rot_matrix(angle_radians):
    return np.matrix([
        [math.cos(angle_radians),-math.sin(angle_radians),0],
        [math.sin(angle_radians), math.cos(angle_radians),0],
        [0,0,1]
    ])
def get_translation_matrix(x,y):
    return np.matrix([
        [1,0,x],
        [0,1,y],
        [0,0,1]
    ])
def get_scaling_matrix(scalex,scaley):
    return np.matrix([
        [scalex,0,0],
        [0,scaley,0],
        [0,0,1]
    ])

def get_point(x,y):
    return np.matrix([
        [x],
        [y],
        [1]
    ])

def symbolSize_to_connectionline_offset(symbolsize, ctype):
    if ctype == 0:
        return symbolsize/6/math.cos(math.pi/6)
    else:
        return symbolsize
    

def draw_start(x,y,a,size,symbolLineWidth):

    tm = get_translation_matrix(x,y)
    r1 = get_rot_matrix(a + (2.0 * math.pi*0.0/3.0))
    r2 = get_rot_matrix(a + (2.0 * math.pi*1.0/3.0))
    r3 = get_rot_matrix(a + (2.0 * math.pi*2.0/3.0))
    tp = get_point(size/6/math.cos(math.pi/6),0)
    p1 =  tm * r1 * tp 
    p2 =  tm * r2 * tp 
    p3 =  tm * r3 * tp 
   
    return drawsvg.Lines(p1[0,0],p1[1,0],p2[0,0],p2[1,0],p3[0,0],p3[1,0],close=True, stroke=coursePrintColor,stroke_width=symbolLineWidth,fill="none")
    
def draw_control(x,y,size,symbolLineWidth,gaps,gap_rotation):
    radius = size
    gapcount = len(gaps)
    if gapcount == 0:
        return drawsvg.Circle(x,y,radius,stroke=coursePrintColor, stroke_width=symbolLineWidth,fill="none")
    #return drawsvg.Arc(x,y,radius,10,80,stroke=coursePrintColor,stroke_width=symbolLineWidth,fill="none")
    arcs = drawsvg.Group()
    for i in range(gapcount):
        
        s = (-gaps[i]["startAngle"]+gap_rotation-gaps[i]["distance"]) * 180 / math.pi
        e = (-gaps[(i+1)%gapcount]["startAngle"]+gap_rotation) * 180 / math.pi
        arcs.append(drawsvg.Arc(x,y,radius,s,e,stroke=coursePrintColor,stroke_width=symbolLineWidth,fill="none"))
    return arcs
    
def draw_finish(x,y,size,symbolLineWidth):
    r1 = size
    r2 = size -3*symbolLineWidth
    finish_group = drawsvg.Group()
    finish_group.append(drawsvg.Circle(x,y,r1,stroke=coursePrintColor, stroke_width=symbolLineWidth,fill="none"))
    finish_group.append(drawsvg.Circle(x,y,r2,stroke=coursePrintColor, stroke_width=symbolLineWidth,fill="none"))
    return finish_group

def draw_connectionLines_predefined(connectionLines,transformationmatrix,linewidth):
    lines = drawsvg.Group()
    for connectionLine in connectionLines:
        ps = get_point(
            connectionLine["start"]["x"],
            connectionLine["start"]["y"]
            )
        pe = get_point(
            connectionLine["end"]["x"],
            connectionLine["end"]["y"]
            )
        ms = transformationmatrix * ps
        me = transformationmatrix * pe
        lines.append(drawsvg.Line(ms[0,0],ms[1,0],me[0,0],me[1,0],stroke=coursePrintColor, stroke_width=linewidth))
    return lines

def draw_connectionLines_calculate(c1x, c1y, c1t, sS1, c2x, c2y, c2t, sS2, connectionlinewidth):
    c1 = get_point( symbolSize_to_connectionline_offset(sS1,c1t),0)
    c2 = get_point(-symbolSize_to_connectionline_offset(sS2,c2t),0)

    r =  math.atan2(c2y-c1y,c2x-c1x)
    rm = get_rot_matrix(r)
    t1 = get_translation_matrix(c1x,c1y)
    t2 = get_translation_matrix(c2x,c2y)

    p1 = t1 * rm * c1
    p2 = t2 * rm * c2

    return drawsvg.Line(p1[0,0],p1[1,0],p2[0,0],p2[1,0],stroke=coursePrintColor, stroke_width=connectionlinewidth)


def draw_controlNumber(x,y,number,transformationmatrix):

    size = 55
    spacing = 0.7
    p = transformationmatrix * get_point(x,y)
    px = p[0,0]
    py = p[1,0]
    gn = drawsvg.Group()
    
    #gn.append(drawsvg.Circle(px,py,5,stroke="none",fill="#00FF00"))
    number_str = str(number)
    numbers = []
    
    sx = 0
    number_count = len(number_str)
    for i in range(number_count):
        c = number_str[i]
        n = int(c)
        numbers.append(n)
        offset_x,_ = svg_numbers[n]
        
        sx += offset_x*size*0.5*((i == 0) + ((i+1) == number_count))

    sx += (number_count-1)*size*spacing
    
    px -= sx/2
    py -= size/2
    for n in numbers:
        offset_x,data = svg_numbers[n]

        og = drawsvg.Group(transform=f"translate({px},{py}),scale({size})")
        og.append(drawsvg.Path(d=data,fill=coursePrintColor,stroke="none"))
        gn.append(og)
        px += size * spacing

    return gn


def generate_CoursePrint(map,course):


    h = map["height"]
    w = map["width"]
    dpm = np.matrix(map["projection"]["matrix"])
    resolution = map["resolution"]
    rotation = map["rotation"]*math.pi/180

    sm = get_scaling_matrix(1/resolution,1/resolution)

    pm = sm * dpm


    d = drawsvg.Drawing(w/resolution,h/resolution)


    controls = course["controls"]
    connectionlinewidth = course.get("controlConnectionLineWidth",default_controlConnectionLineWidth)
    controlNumber = 0


    for i in range(len(controls)):
        control = controls[i]
        nextcontrol = None
        ctype = control["control"]["type"]
        if ctype == 1:
            controlNumber += 1
        px = control["control"]["projectedPosition"]["x"]
        py = control["control"]["projectedPosition"]["y"]
        pP = np.matrix([[px],[py],[1]])
        

        symbolSize = control["control"].get("symbolSize",default_symbolSize[ctype])
        symbolLineWidth = control["control"].get("symbolLineWidth",default_symbolLineWidth)
        mP = pm * pP

        circleGaps = control["control"].get("circleGaps",[])

        start_rotation = 0

        if (i+1)<len(controls):
            nextcontrol = controls[i+1]
            nextctype = nextcontrol["control"]["type"]
            nextsymbolSize = nextcontrol["control"].get("symbolSize",default_symbolSize[nextctype])
            npx = nextcontrol["control"]["projectedPosition"]["x"]
            npy = nextcontrol["control"]["projectedPosition"]["y"]
            pNP = np.matrix([[npx],[npy],[1]])
            mNP = pm * pNP
            nca = math.atan2(mNP[1,0]-mP[1,0],mNP[0,0]-mP[0,0])
            start_rotation = nca

        if "projectedConnectionLines" in control:
            d.append(draw_connectionLines_predefined(control["projectedConnectionLines"],pm,connectionlinewidth))
        elif nextcontrol is not None:
            d.append(draw_connectionLines_calculate(mP[0,0],mP[1,0],ctype, symbolSize, mNP[0,0],mNP[1,0], nextctype, nextsymbolSize, connectionlinewidth))


        if "controlNumberProjectedPosition" in control:
            d.append(draw_controlNumber(control["controlNumberProjectedPosition"]["x"], control["controlNumberProjectedPosition"]["y"], controlNumber, pm))

        if ctype == 0:
            d.append(draw_start(mP[0,0],mP[1,0] ,start_rotation,symbolSize,symbolLineWidth))
        elif control["control"]["type"] == 1:
            d.append(draw_control(mP[0,0],mP[1,0],symbolSize,symbolLineWidth,circleGaps,rotation))
        elif control["control"]["type"] == 2:
            d.append(draw_finish(mP[0,0],mP[1,0],symbolSize,symbolLineWidth))
    return d.as_svg()

def get_svg_url_fromCourseImages(course):
    urls = []
    for courseImage in course["courseImages"]:
        urls.append(courseImage["url"])

    return urls


def hasCourseImage(course):
    if "courseImages" in course:
        if len(course["courseImages"]) > 0:
            return True
    return False

def applyCoursePrintToMap(map,coursePrint):
    base_img = Image.open(io.BytesIO(map)).convert("RGBA")
    w,h = base_img.size

    CoursePrintRaster_bytes = cairosvg.svg2png(bytestring=(coursePrint),
                                output_width=w,  # target width
                                output_height=h) # target height    
    CoursePrintRaster = Image.open(io.BytesIO(CoursePrintRaster_bytes)).convert("RGBA")
    a = io.BytesIO()
    base_img.paste(CoursePrintRaster,(0,0),CoursePrintRaster)
    base_img.save(a,"png")
    return a.getvalue()

def saveimg(name,img, pgw=None):
    with open(name+".png","wb") as image:
        image.write(img)
    if pgw is not None:
        pgw.write(name+".pgw")

def parseargs():
    parser = argparse.ArgumentParser(description="Downloads Maps from livelox.com")
    parser.add_argument("urlorclassid",help="url to livelox event or classId")
    parser.add_argument("operation",type=str,choices=["mapOnly","mapCourse"],help="Specify operation\n\tmapOnly = Only the map\n\tcourseSingle = Saves all the courses to indiviual images, useful for forked courses\n\tcourseCombine = Saves all the courses to one file, all forks on the same map")
    parser.add_argument("-N","--name",type=str, required = False,help="Name of the map, defaults to the name provided by livelox",default="")
    parser.add_argument("-P","--password",type=str,required=False, help="Some activities require password",default="")
    parser.add_argument("-C","--saveClassBlob",action='store_true',help="Save ClassBlob jsonfile")
    return parser.parse_args()

def get_coursePrintsAndNames(map,courses):
    courseImagesNames = []
    
    for course in courses:
        courseImage = None
        courseName = course["name"]
        if hasCourseImage(course):
            urls = get_svg_url_fromCourseImages(course)
            r_svg = session.get(urls[0])
            if r_svg.ok:
                courseImage = r_svg.content

        else:
            courseImage = generate_CoursePrint(map,course)
        courseImagesNames.append((courseImage,courseName))
    return courseImagesNames


def get_classId(args):
    class_id = 0
    try:
        class_id = int(args.urlorclassid)
    except:
        query = urlparse(args.urlorclassid).query
        params = parse_qs(query)
        class_id = params.get('classId', [None])[0]
    return class_id

def save_courseSingle(image_map,courseImagesNames,mapName,pgw=None):
    for courseImage, courseName in courseImagesNames:
        final = applyCoursePrintToMap(image_map,courseImage)
        fullName = mapName + "_" + courseName
        saveimg(fullName,final,pgw)



args = parseargs()

class_id = get_classId(args)


ajax_headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Content-Type": "application/json",
    "Origin": "https://www.livelox.com",
    "X-Requested-With": "XMLHttpRequest"
}


payload = {"classIds":[class_id],"includeMap":True,"eventPassword":args.password,"includeCourses":True}

r2 = session.post("https://www.livelox.com/Data/ClassBlob",json=payload,headers=ajax_headers)
print(f"ClassBlob status: {r2.status_code}")


if not r2.ok:
    exit(1)


jsondata = r2.json()



pgw = PGW(jsondata)

mapName = (jsondata["map"]["name"] if args.name == "" else args.name) +"_"+pgw.type


if args.saveClassBlob:
    with open(f"{mapName}_ClassBlob.json","wb") as f:
        f.write(r2.content)



image_map = session.get(jsondata["map"]["url"]).content


if args.operation == "mapCourse":
    courseImagesNames = get_coursePrintsAndNames(jsondata["map"],jsondata["courses"])
    save_courseSingle(image_map,courseImagesNames,mapName,pgw)
else:
    fullName = mapName
    saveimg(fullName,image_map,pgw)


