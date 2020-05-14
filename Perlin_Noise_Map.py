from PIL import Image
from PIL import ImageFilter

import math
import noise
import decimal
import numpy as np
import cv2

from shapely.geometry import MultiPoint
from shapely.ops import triangulate

import geopandas as gpd
from shapely.geometry import Polygon
from shapely.geometry import MultiPolygon
from bisect import bisect_left

import matplotlib.pyplot as plt

def take_closest(myList, myNumber):
    pos = bisect_left(myList, myNumber)
    if pos == 0:
        return myList[0]
    if pos == len(myList):
        return myList[-1]
    before = myList[pos - 1]
    after = myList[pos]
    if after - myNumber < myNumber - before:
       return after
    else:
       return before

def drange(x, y, jump):
  while x <= y:
    yield float(x)
    x = decimal.Decimal(str(x)) + decimal.Decimal(jump)

def triangulatePoints(polygon):
    return [triangle for triangle in triangulate(polygon) if triangle.within(polygon)]

def vecpointsToPoints(contourList):
    ret = []
    i = 0
    for contour in contourList:
        ret.append([])
        for point in contour:
            ret[i].append((point[0][0], point[0][1]))
        if (len(ret[i]) < 3):
            ret.pop()
        else:
            i+=1
    return ret

def genTerrain(size, scale):

    dimensions = (size, size)
    octaves = 5
    persistence = 0.5
    lacunarity = 2.0
    offset = 0.5

    noiseMap = np.zeros(dimensions)

    for i in range(dimensions[0]):
        for j in range(dimensions[1]):
            noiseMap[i][j] = (noise.snoise2(
                                        i/scale, 
                                        j/scale, 
                                        octaves=octaves, 
                                        persistence=persistence, 
                                        lacunarity=lacunarity, 
                                        repeatx=size, 
                                        repeaty=size, 
                                        base=0) + offset)
    return noiseMap

def getColorDict(k):
    colors = {}
    colorIncrement = 255.0 / (k-1)
    n = 0.0
    incrementor = 1 / k
    for i in drange(0, 255.0, colorIncrement):
        colors[round(n, 2)] = ((i,) * 3)
        n += incrementor
    return colors

def colorNoiseMap(noiseMap, numberOfColors):
    noiseMapColored = np.zeros(noiseMap.shape+(3,), dtype=np.uint8)
    colorDict = getColorDict(numberOfColors)

    buckets = [round(x, 2) for x in drange(0.0, 1.0, 1/numberOfColors)]

    for i in range(noiseMap.shape[0]):
        for j in range(noiseMap.shape[1]):
            bucket = take_closest(buckets, noiseMap[i][j])
            noiseMapColored[i][j] = colorDict.get(bucket)
    return noiseMapColored

print("\ncreating noise map...\n")
noiseMap = genTerrain(2048, 1500)

print("coloring noise map...\n")
noiseMapColored = colorNoiseMap(noiseMap, 5)

img1 = Image.fromarray(noiseMap)
img1.save('noise.tiff')

img2 = Image.fromarray(noiseMapColored)
img2.save('colorNoise.tiff')

print("getting water boundaries...\n")

img = cv2.imread('colorNoise.tiff')
inverted_image = cv2.bitwise_not(img)
imGray = cv2.cvtColor(inverted_image, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imGray, 200, 255, 0)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

img = cv2.drawContours(img, contours, -1, (0,0,255), 1, 4)
img = Image.fromarray(img)
img.save('test.tiff')

lakes = vecpointsToPoints(contours)

print("triangulating and storing boundaries in wavefront obj file...\n")

vertices = []
polygons = []

for lake in lakes:
    lakePoly = Polygon(lake)
    if (lakePoly.is_valid):
        lakeTriangles = triangulatePoints(lakePoly)
        for t in lakeTriangles:
            v = list(t.exterior.coords)

            v1 = (v[0][0], v[0][1], 0.0)
            v2 = (v[1][0], v[1][1], 0.0)
            v3 = (v[2][0], v[2][1], 0.0)

            vertices.append(v1)
            vertices.append(v2)
            vertices.append(v3)

            size = len(vertices)

            polygons.append((size-2,size-1,size))

f = open("water.obj", "w")

for v in vertices:
    f.write("v "+str(v[0])+" "+str(v[1])+" "+str(v[2])+"\n")

f.write("\nvn 0.0 1.0 0.0\n\n")

for p in polygons:
    f.write("f "+str(p[0])+"//1 "+str(p[1])+"//1 "+str(p[2])+"//1\n")
f.close()

print("done!\n")
