import sys
import math

# first guess: 4613357005 too high
# second guess: 4613357005

maxX = 0
maxY = 0
minX = 9999999
minY = 9999999
reds = set()
xPointsCache = {}
yPointsCache = {}

def readPoints(filename):
    points = []
    global maxX, maxY, minX, minY
    with open(filename,'r') as f:
        for l in f.readlines():
            line = l.strip()
            x,y = line.split(",")
            x = int(x)
            y = int(y)
            maxX = max(x, maxX)
            minX = min(x, minX)
            maxY = max(y, maxY)
            minY = min(y, minY)
            yield(x,y)


def calculateArea(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    width = abs(x1-x2) + 1
    height = abs(y1-y2) + 1
    return width * height

def translatePoints(points):
    global maxX, maxY, minX, minY
    newPoints = []
    for x,y in points:
        newPoints.append((x-minX, y-minY))

    maxX -= minX
    maxY -= minY
    minX = 0
    minY = 0
    return newPoints

def buildGrid(pointSet, maxX, maxY):
    grid = []
    for y in range(maxY+1):
        row = ['.'] * (maxX+1)
        grid.append(row)
    for x, y in pointSet:
        grid[y][x] = 'X'
        if (x,y) in reds:
            grid[y][x] = '#'
    return grid


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
    global reds
    pointSet = set()
    reds = set(points)
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

def compress(pointList, fixed, XorY):
    # print("Compress Input:", pointList)
    if XorY == 'X':
        values = [y[1] for y in pointList]
    else:
        values = [x[0] for x in pointList]

    values.sort()

    # print("Compress Values PRE:", values)

    last = -1
    newValues = []
    for v in values:
        if last == -1 or v - last > 1:
            newValues.append(v)
        last = v

    # print("Compress Values POST:", newValues)
    
    if XorY == 'X':
        result= [(fixed, v) for v in newValues]
    else:
        result= [(v, fixed) for v in newValues]
    # print("Compress Output:", result) 
    return result

def getXPoints(pointSet, x):
    if x in xPointsCache:
        return xPointsCache[x]
    xPoints = [k for k in pointSet if k[0] == x]
    xPoints = compress(xPoints, x, 'X')
    xPointsCache[x] = xPoints
    return xPoints

def getYPoints(pointSet, y):
    if y in yPointsCache:
        return yPointsCache[y]
    yPoints = [k for k in pointSet if k[1] == y]
    yPoints = compress(yPoints, y, 'Y')
    yPointsCache[y] = yPoints
    return yPoints

def isPointInPolygon(pointSet, p):
    # print("Testing:", p)
    if p in pointSet:
        return True
    x,y = p
    xPoints = getXPoints(pointSet, x)
    yPoints = getYPoints(pointSet, y)
    # print(p, xPoints, yPoints)
    oneAbove = len([p for p in xPoints if p[1] < y]) % 2 == 1
    oneBelow = len([p for p in xPoints if p[1] > y]) % 2 == 1
    oneLeft = len([p for p in yPoints if p[0] < x]) % 2 == 1
    oneRight = len([p for p in yPoints if p[0] > x]) % 2 == 1
    # print("Above:", oneAbove, "Below:", oneBelow, "Right:", oneRight, "Left:", oneLeft)
    return oneAbove and oneBelow and oneLeft and oneRight

def isInPolygon(pointSet, p1,p2):
    print("Testing", p1, p2)
    p3 = (p1[0], p2[1])
    p4 = (p2[0], p1[1])
    toTest = buildPolygonPointSet([p1,p2,p3,p4])
    for p in toTest:
        if not isPointInPolygon(pointSet, p):
            return False
        
    # print(pointSet)
    return True

def printGrid(grid):
    for y in grid:
        for x in y:
            print(x, end='')
        print()
           
if __name__ == "__main__":
    points = list(readPoints(sys.argv[1]))
    #points = translatePoints(points)
    areas = getAreaList(points)
    pointSet = buildPolygonPointSet(points)
    #grid = buildGrid(pointSet, maxX, maxY)
    #printGrid(grid)
    for area, p1, p2 in areas:
        if isInPolygon(pointSet, p1, p2):
            print(area)
            exit(0)

    


