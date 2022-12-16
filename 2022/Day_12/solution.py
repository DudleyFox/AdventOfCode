# 450 was too high

def readMap():
    topo = []
    with open('input.txt','r') as f:
        for x in f.readlines():
            topo.append([i for i in x.strip()])
    return topo

def getStartPoint(topo):
    y = 0
    x = 0
    for line in topo:
        x = 0
        for p in line:
            if p == 'S':
                return (x,y)
            x += 1
        y += 1
    raise Exception('No starting point found')

def getHeight(x,y, topo):
    a = topo[y][x]
    if a == 'E':
        return ord('z')
    elif a == 'S':
        return ord('a')
    return ord(a)

def isValidLocation(x,y, oldX, oldY, maxX, maxY, topo, visited):
    # print('isValidLocation:',x,y,oldX,oldY,maxX,maxY)
    if x < 0 or x >= maxX:
        return False
    if y < 0 or y >= maxY:
        return False

    currentHeight = getHeight(oldX, oldY, topo)
    newHeight = getHeight(x,y,topo)

    # print('Heights',currentHeight, newHeight)

    if currentHeight < (newHeight - 1):
        return False

    return (x,y) not in visited
    

def getAvailableLocations(x,y,maxX, maxY, topo, visited):
    locations = []
    # up
    locations.append((x, y - 1)) 
    # down
    locations.append((x, y + 1))
    # left
    locations.append((x - 1, y))
    # right
    locations.append((x + 1, y))

    return [(i,j) for i,j in locations if isValidLocation(i,j, x,y, maxX, maxY, topo, visited) ]


# def shortPathR(x,y,maxX, maxY, topo, visited, distance, pathTaken):
#     print('Current:',x,y)
#     visited.add((x,y))
#     pt = [x for x in pathTaken]
#     pt.append((x,y))
#     if topo[y][x] == 'E':
#         return (distance, pt)
#     locations = getAvailableLocations(x,y,maxX, maxY, visited)
#     # print('New paths:', locations)
#     if len(locations) == 0: # dead end
#         return (-1, [])
#     distances = [shortPathR(i,j, maxX, maxY, topo, visited, distance + 1, pt) for i,j in locations]
#     # print('Distances:',distances)
#     distances = [i for i in distances if i[0] > 0]
#     distances.sort(key=lambda i: i[0])
#     if len(distances) == 0:
#         return (-1, [])
#     return distances[0]

def buildPaths(paths, maxX, maxY, topo, visited):
    pathsInFlight = [p for p in paths]
    completePaths = []
    while len(pathsInFlight) > 0:
        tmp = pathsInFlight
        pathsInFlight = []
        for t in tmp:
            x,y = t[-1]
            locations = getAvailableLocations(x,y, maxX, maxY, topo, visited)
            for i,j in locations:
                newT = list(t)
                newT.append((i,j))
                if topo[j][i] == 'E':
                    completePaths.append(newT)
                else:
                    visited.add((i,j))
                    pathsInFlight.append(newT)
    distances = [len(p) for p in completePaths]
    distances.sort()
    return distances[0] - 1



def getShortestPath(x,y,topo):
    maxX = len(topo[0])
    maxY = len(topo)
    visited = set()
    pathsTaken = [[(x,y)]]
    visited.add((x,y))
    return buildPaths(pathsTaken, maxX, maxY, topo, visited)

if __name__ == '__main__':
    topo = readMap()
    x, y = getStartPoint(topo)
    distance = getShortestPath(x,y,topo)
    print(distance)

