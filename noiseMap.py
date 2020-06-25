import click
import noise
import os
import numpy as np
from PIL import Image

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

def genNoiseMap(size, scale):
    dimensions = (size, size)
    octaves = 8
    persistence = 0.5
    lacunarity = 2.0
    offset = 0.5

    noiseMap = np.zeros(dimensions)

    for i in range(dimensions[0]):
        for j in range(dimensions[1]):
            noiseMap[i][j] = int((
                noise.snoise2(
                i/scale, 
                j/scale, 
                octaves=octaves, 
                persistence=persistence, 
                lacunarity=lacunarity, 
                repeatx=size, 
                repeaty=size, 
                base=0) + offset) * 255)
    return noiseMap

@click.command()
@click.option('-l', 'levels', default=-1, help='number of bit levels')
@click.option('-o', 'output_filename', default='output.png', help='output file')
@click.argument('size', type=click.INT)
@click.argument('scale', type=click.INT)
def noiseMap(size, scale, levels, output_filename):
    noiseMap = genNoiseMap(size, scale)
    noiseMap = Image.fromarray(noiseMap)
    noiseMap = noiseMap.convert('L')

    if (levels != -1):
        #noiseMap = ImageOps.posterize(noiseMap, levels)
        noiseMap= noiseMap.quantize(levels)

    noiseMap.save(getUniqueFileName(output_filename))

if __name__ == '__main__':
    noiseMap()
