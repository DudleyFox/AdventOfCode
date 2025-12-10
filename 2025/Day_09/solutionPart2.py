import sys
import math

# first guess: 4613357005 too high

def readPoints(filename):
    points = []
    with open(filename,'r') as f:
        for l in f.readlines():
            line = l.strip()
            x,y = line.split(",")
            x = int(x)
            y = int(y)
            yield(x,y)


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

def addLine(pointSet, p1, p2):
    pointSet.add(p1)
    pointSet.add(p2)
    x1, y1 = p1
    x2, y2 = p2
    if x1 == x2:
        if y1 < y2:
            for j in range(y1, y2+1):
                pointSet.add((x1,j))
        else:
            for j in range(y2, y1+1):
                pointSet.add((x1,j))
    else:
        if x1 < x2:
            for j in range(x1, x2+1):
                pointSet.add((j,y1))
        else:
            for j in range(x2, x1+1):
                pointSet.add((j,y1))

def buildPolygonPointSet(points):
    pointSet = set()
    firstPoint = points[0]
    lastPoint = points[-1]
    for i in range(len(points) - 1):
        p1 = points[i]
        p2 = points[i+1]
        addLine(pointSet, p1, p2)
        # print("Added:", p1, p2, pointSet)
    addLine(pointSet, lastPoint, firstPoint)
    return pointSet

def fillPolygon(pointSet):
    pass

def isPointInPolygon(pointSet, p):
    # print("Testing:", p)
    if p in pointSet:
        return True
    x,y = p
    xPoints = [p for p in pointSet if p[0] == x]
    yPoints = [p for p in pointSet if p[1] == y]
    # print(p, xPoints, yPoints)
    oneAbove = len([p for p in xPoints if p[1] <= y]) > 0
    oneBelow = len([p for p in xPoints if p[1] >= y]) > 0
    oneLeft = len([p for p in yPoints if p[0] <= x]) > 0
    oneRight = len([p for p in yPoints if p[0] >= x]) > 0
    # print("Above:", oneAbove, "Below:", oneBelow, "Right:", oneRight, "Left:", oneLeft)
    return oneAbove and oneBelow and oneLeft and oneRight

def isInPolygon(pointSet, p1,p2):
    # print("*************\nTesting", p1, p2)
    p3 = (p1[0], p2[1])
    p4 = (p2[0], p1[1])
    toTest = [p1,p2,p3,p4]
    for p in toTest:
        if not isPointInPolygon(pointSet, p):
            return False
        
    # print(pointSet)
    return True
           
if __name__ == "__main__":
    points = list(readPoints(sys.argv[1]))
    areas = getAreaList(points)
    pointSet = buildPolygonPointSet(points)
    for a in areas:
        area, p1, p2 = a
        if isInPolygon(pointSet, p1, p2):
            print(area)
            exit(0)

    


