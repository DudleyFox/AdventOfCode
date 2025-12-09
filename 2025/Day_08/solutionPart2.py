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
        
def getCircuit(circuits, p1, p2):
    activeCircuits = []
    for i in range(len(circuits)):
        circuit = circuits[i]
        if p1 in circuit or p2 in circuit:
            activeCircuits.append((i, circuit))

    acl = len(activeCircuits)
    if acl == 0:
        s = set()
        print("acl:", acl, s)
        circuits.append(s)
        return s
    elif acl == 1:
        s = activeCircuits[0][1]
        print("acl:", acl, s)
        return s
    elif acl == 2:
        del circuits[activeCircuits[1][0]] # delete the last one first
        del circuits[activeCircuits[0][0]] # delete the first one last
        s = activeCircuits[0][1].union(activeCircuits[1][1])
        circuits.append(s)
        print("acl:", acl, s)
        return s


def buildCircuits(distanceList, points):
    circuits = [set([x]) for x in points]
    for distance, p1, p2 in distanceList:
        print("Connecting:", p1, p2)
        s = getCircuit(circuits, p1, p2)
        s.add(p1)
        s.add(p2)
        if len(circuits) == 1:
            print(p1[0], p2[0], p1[0] * p2[0])
            break
        print("Connected:", s)
        print()
    return circuits

            


if __name__ == "__main__":
    points = list(readPoints(sys.argv[1]))
    sortedList = buildDistanceList(points)
    circuits = buildCircuits(sortedList, points)
    



    


