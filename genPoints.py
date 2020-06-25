import click
import cv2
import os
import decimal
import numpy as np
import PoissonDisk as pd
from PIL import Image, ImageDraw

def getUniqueFileName(filename):
    i = 1
    fn = filename.split('.')
    if os.path.isfile(filename):
        while(1):
            newFilename = fn[0]+str(i)+'.'+fn[1]
            if os.path.isfile(newFilename):
                i += 1
            else: 
                break
        filename = newFilename
    return filename

def drange(x, y, jump):
  while x < y:
    yield float(x)
    x = decimal.Decimal(str(x)) + decimal.Decimal(jump)

def lerpColor(c1, c2, t):
    return (c1 + t * (c2 - c1)).astype(int)

def lerp(n1, n2, t):
    return n1 + t * (n2 - n1)

def getLevels(image, nmbLevels):

    img = Image.open(image)

    img = img.quantize(nmbLevels)
    tmpLevels = img.getpalette()

    levels = [] 

    for i in range(0, len(tmpLevels), 3):
        levels.append(tmpLevels[i])
        if (len(levels) >= nmbLevels): break

    return levels

def getColorGrad(max, min, granularity):
    colors = []
    foo = 1/(granularity-1)
    for i in drange(0.0, 1.0 + foo, foo):
        colors.append(tuple(lerpColor(max, min, i)))
    return colors

def getRadiusGrad(max, min, granularity):
    radius = []
    foo = 1/(granularity-1)
    for i in drange(0, 1 + foo, foo):
        radius.append(round(lerp(max, min, i)))
    return radius

def filterPoints(points, sizeList, nmbLevels, mask_filename):

    filteredPoints = []

    mask = cv2.imread(mask_filename)

    levels = getLevels(mask_filename, nmbLevels)

    for p in points:
        coord = int(p[1]), int(p[0])

        brightness = mask[coord][0]
        i = 0
        addPoint = False
        for l in levels:
            if (brightness >= l):
                i = levels.index(l)
                addPoint = True
                break

        if (addPoint):
            filteredPoints.append((p[0], p[1], sizeList[i]))

    return filteredPoints

def drawPointsToImage(image_filename, points, radiusList, colorList, nmbLevels):

    img = Image.open(image_filename)
    output_image = Image.new("RGB", img.size)
    draw = ImageDraw.Draw(output_image)

    mask = cv2.imread(image_filename)

    levels = getLevels(image_filename, nmbLevels)

    for p in points:

        coord = int(p[1]), int(p[0])
        i = 0
        drawObj = False
        brightness = mask[coord][0]

        for l in levels:
            if (brightness >= l):
                i = levels.index(l)
                drawObj = True
                break

        if (drawObj):
            draw.ellipse((int(p[0]) - radiusList[i], 
                          int(p[1]) - radiusList[i], 
                          int(p[0]) + radiusList[i], 
                          int(p[1]) + radiusList[i]), 
                          fill=colorList[i], 
                          outline =colorList[i])
    return output_image

def savePointsToFile(points, fileName):
    file = open(fileName, "w")
    # xpos ypos size
    for p in points:
        file.write(str(p[0])+" "+str(p[1])+" "+str(p[2])+"\n")

@click.command()
@click.option('-o', 'output_filename', default='output.txt', help='output file')
@click.option('-c', 'colors', default=((0,)*3,(255,)*3), type=(int, int, int), multiple=True, help='colors for points')
@click.option('-r', 'radii', nargs=2, default=(5, 1), type=click.INT, help='max/min radii')
@click.option('-sampleRadius', 'sampleRadius', default=10, type=click.INT, help='sample radius for poisson')
@click.option('-rejectionSamples', 'rejectionSamples', default=10, type=click.INT, help='number of rejection samples for poisson')
@click.argument('mask_filename', type=click.Path(exists=True))
@click.argument('levels', type=click.INT)
def genPoints(mask_filename, output_filename, sampleRadius, rejectionSamples, levels, colors, radii):
    mask = cv2.imread(mask_filename)

    sampleRegionSize = np.array([mask.shape[0], mask.shape[1]])
    grassPoints = pd.PoissonDiskSampling(sampleRadius, sampleRegionSize, rejectionSamples)

    maxc, minc = colors
    maxr, minr= radii

    colorList = getColorGrad(np.array(maxc), np.array(minc), levels)
    radiiList = getRadiusGrad(maxr, minr, levels)

    filteredGrassPoints = filterPoints(grassPoints, radiiList, levels, mask_filename)
    savePointsToFile(filteredGrassPoints, getUniqueFileName(output_filename))

    colorPoints = drawPointsToImage(mask_filename, filteredGrassPoints, radiiList, colorList, levels)
    colorPoints.show()
    colorPoints.save(getUniqueFileName('img.png'))

if __name__ == '__main__':
    genPoints()
