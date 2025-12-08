import sys
import math


def readPoints(filename):
    with open(filename,'r') as f:
        for l in f.readlines():
            line = l.strip()
            x,y,z = line.split(",")
            yield (int(x), int(y), int(z))

def calculateDistance(p1, p2):
    x1,y1,z1 = p1
    x2,y2,z2 = p2
    total = (x1 - x2) ** 2 + (y1-y2) ** 2 + (z1-z2) ** 2
    return math.sqrt(total)

def buildDistanceList(points):
    ptsLent = len(points)
    distanceList = []
    for i in range(ptsLent):
        for j in range(i+1, ptsLent):
            p1= points[i]
            p2= points[j]
            distance = calculateDistance(p1,p2)
            distanceList.append((distance, p1, p2))

    distanceList.sort(key=lambda element: element[0])
    return distanceList
            


            


if __name__ == "__main__":
    if len(sys.argv) > 2:
        iterations = int(sys.argv[2])
    else:
        iterations = 40
    points = list(readPoints(sys.argv[1]))
    sortedList = buildDistanceList(points)
    for s in sortedList[:iterations]:
        print(s)


