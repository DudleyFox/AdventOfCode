import itertools

def updateDistanceMap(c1,c2,dMap,d):
    if c1 not in dMap:
        dMap[c1] = {c2:d}
    else:
        dMap[c1][c2] = d
    if c2 not in dMap:
        dMap[c2] = {c1:d}
    else:
        dMap[c2][c1] = d

def readData():
    cities = set()
    distanceMap = {}
    with open('input.txt', 'r') as f:
        for l in f.readlines():
            c1, t, c2, e, distance = l.strip().split(' ')
            cities.add(c1)
            cities.add(c2)
            updateDistanceMap(c1, c2, distanceMap, int(distance))
        return (cities, distanceMap)

def calculuteDistance(route, distanceMap):
    distance = 0
    for c1, c2 in itertools.pairwise(route):
        distance += distanceMap[c1][c2]
    return distance

def findShortest(cities, distanceMap):
    shortest = 999999
    for route in itertools.permutations(cities):
        shortest = min(calculuteDistance(route, distanceMap), shortest)
    return shortest

if __name__ == '__main__':
    cities, distanceMap = readData()
    print(findShortest(cities, distanceMap))


