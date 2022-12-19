

def readData():
    rawData = []
    with open('input.txt', 'r') as f:
        for x in f.readlines():
            rawData.append(x.strip())
    print(rawData)
    return rawData

def transformToIntTuples(data):
    polishedData = []
    for line in data:
        pairs = line.split(' -> ')
        tuples = []
        for p in pairs:
            xAndY = [int(x) for x in p.split(',')]
            tuples.append((xAndY[0], xAndY[1]))
        polishedData.append(tuples)
    print(polishedData)
    return polishedData

def translateData(data):
    maxX = 0
    maxY = 0
    minX = 500
    minY = 0
    
    for d in data:
        for x,y in d:
            maxX = max(x, maxX)
            maxY = max(y, maxY)
            minX = min(x, minX)
            minY = min(y, minY)

    minX -= 2 # make space for sand

    newData = []
    for d in data:
        tuples = []
        for x, y in d:
            tuples.append((x-minX, y-minY))
        newData.append(tuples)

    return (minX, minY, maxX-minX, maxY-minY, 500 - minX, 0 - minY, newData)

def buildEmptyCavern(maxX, maxY):
    cavern = []
    for y in range(maxY):
        line = []
        for x in range(maxX):
            line.append('.')
        cavern.append(line)
    return cavern

def order(x1,x2):
    if x1 < x2:
        return (x1,x2)
    return (x2, x1)


def addRockLine(p1, p2, cavern):
    x1, y1 = p1
    x2, y2 = p2

    x1, x2 = order(x1, x2)
    y1, y2 = order(y1, y2)
    for y in range(y1,y2+1):
        for x in range(x1,x2+1):
            cavern[y][x] = '#'

def addRockHelper(cavern, line):
    last = line[0]
    for point in line:
        addRockLine(last, point, cavern)
        last = point

def addRocks(cavern, rockData):
    for d in rockData:
        addRockHelper(cavern, d)

def printCavern(cavern):
    for y in cavern:
        for x in y:
            print(x, end='')
        print()
    print('=====================')

class Sand:
    def __init__(self, cavern, origin, maxY):
        self.cavern = cavern
        self.x = origin[0]
        self.y = origin[1]
        self.startVoid = maxY
        self.inMotion = True

    def inVoid(self):
        return self.y >= self.startVoid

    def tick(self):
        if cavern[self.y+1][self.x] == '.':
            cavern[self.y][self.x] = '.'
            cavern[self.y+1][self.x] = 'O'
            self.y += 1
        elif cavern[self.y+1][self.x-1] == '.':
            cavern[self.y][self.x] = '.'
            cavern[self.y+1][self.x-1] = 'O'
            self.y += 1
            self.x -= 1
        elif cavern[self.y+1][self.x+1] == '.':
            cavern[self.y][self.x] = '.'
            cavern[self.y+1][self.x+1] = 'O'
            self.y += 1
            self.x += 1
        else:
            self.inMotion = False
        return self.inMotion
        

def runSand(cavern, origin, maxY, sand):
    while True:
        s = Sand(cavern, origin, maxY)
        sand.append(s)
        print('tick')
        while s.tick():
            print('tock')
            if s.inVoid():
                return
            # printCavern(cavern)
            # input('continue?')



if __name__ == '__main__':
    minX, minY, maxX, maxY, oX, oY, data = translateData(transformToIntTuples(readData()))
    print(minX)
    print(minY)
    print(maxX)
    print(maxY)
    print(oX)
    print(oY)
    print(data)
    cavern = buildEmptyCavern(maxX + 2, maxY + 2)
    printCavern(cavern)
    addRocks(cavern, data)
    cavern[oY][oX] = '+'
    printCavern(cavern)
    sand = []
    runSand(cavern, (oX,oY), maxY, sand)
    printCavern(cavern)
    sum = 0
    for s in sand:
        if not s.inMotion:
            sum += 1

    print(sum)

    
        