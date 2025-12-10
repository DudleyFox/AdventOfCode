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


def calculateDistance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def calculateArea(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    width = abs(x1-x2) + 1
    height = abs(y1-y2) + 1
    return width * height
                      


def getLargestArea(points):
    maxArea = 0
    for i in range(len(points)-1):
        for j in range(i+1, len(points)):
            p1 = points[i]
            p2 = points[j]
            area = calculateArea(p1,p2)
            print(p1, p2, area)
            maxArea = max(area, maxArea)

    return maxArea

           
if __name__ == "__main__":
    points = list(readPoints(sys.argv[1]))
    print(getLargestArea(points))
    


