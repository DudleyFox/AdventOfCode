import sys
import math

# first guess: 4442262383
# second guess: 4763932976
def readPoints(filename):
    points = []
    with open(filename,'r') as f:
        for l in f.readlines():
            line = l.strip()
            x,y = line.split(",")
            yield(int(x),int(y))


def calculateArea(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    width = abs(x1-x2) + 1
    height = abs(y1-y2) + 1
    return width * height
                      


def getAreaList(points):
    areaList = []
    for i in range(len(points)-1):
        for j in range(i+1, len(points)):
            p1 = points[i]
            p2 = points[j]
            area = calculateArea(p1,p2)
            areaList.append((area, p1, p2))

    areaList.sort(key=lambda x: x[0], reverse=True)
    return areaList

def testPoint(polygonPoint, pointToTest):
    x,y = polygonPoint
    tX,tY = pointToTest
    if y

def isInPolygon(points, p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = x1, y2
    x4, y4 = x2, y1
    

    for p in points:
        x,y=p

        

           
if __name__ == "__main__":
    points = list(readPoints(sys.argv[1]))
    areas = getAreaList(points)
    for a in areas:
        rectPoints = getRectablePoints(a[1],a[2])

    


