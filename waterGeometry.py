import click
import os
from shapely.geometry import Polygon, MultiPolygon, MultiPoint

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

def triangulatePoints(polygon):
    return [triangle for triangle in triangulate(polygon) if triangle.within(polygon)]

def createWavefrontOBJ(lakes, filename):
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

    f = open(filename, "w")

    for v in vertices:
        f.write("v "+str(v[0])+" "+str(v[1])+" "+str(v[2])+"\n")

    f.write("\nvn 0.0 1.0 0.0\n\n")

    for p in polygons:
        f.write("f "+str(p[0])+"//1 "+str(p[1])+"//1 "+str(p[2])+"//1\n")
    f.close()

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

@click.command()
@click.argument('intput_filename', type=click.Path(exists=True))
@click.option('-o', 'output_filename', default='output.obj', help='output file')
def waterGeometry(intput_filename, output_filename):
    img = cv2.imread(intput_filename)
    inverted_image = cv2.bitwise_not(img)
    imGray = cv2.cvtColor(inverted_image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imGray, 250, 255, cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    img = cv2.drawContours(img, contours, -1, (0,0,255), -3, 4)
    img = Image.fromarray(img)
    img.show()

    lakes = vecpointsToPoints(contours)
    createWavefrontOBJ(lakes, getUniqueFileName(output_filename))

if __name__ == '__main__':
    waterGeometry()
