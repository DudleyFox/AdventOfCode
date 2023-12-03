import sys

nonSymbols = set('0123456789.')

digits = set('0123456789')

def readLines(fileName):
    with open(fileName, 'r') as f:
        for x in f.readlines():
            l = x.strip()
            yield ['.'] + [x for x in l] + ['.']

class PossiblePartNumber:
    def __init__(self, schematic, number, xStart ,xEnd,y):
        self.number = number
        self.xStart = xStart
        self.xEnd = xEnd
        self.y = y
        self.schematic = schematic

    def isPartNumber(self):
        for y in range(self.y - 1, self.y + 2):
            for x in range(self.xStart - 1, self.xEnd + 2):
                c = self.schematic[y][x]
                if c not in nonSymbols:
                    return True
        return False
    
    def isNextTo(self, x, y):
        isInYRange = y == self.y or y == self.y-1 or y == self.y + 1
        isInXRange = x >= self.xStart - 1 and x <= self.xEnd + 1
        # techincally we should check if it not on top of the number itself
        # but that would be a bug, as that is impossible in the input.
        return isInYRange and isInXRange

    
    def __str__(self):
        return str(self.number) + ' ' + str(self.xStart) + ' ' + str(self.xEnd) + ' ' + str(self.y)

def buildSchematic(fileName):
    schematic = [x for x in readLines(fileName)]
    rowLen = len(schematic[0])
    schematic = [['.' for x in range(rowLen)]] + schematic + [['.' for x in range(rowLen)]]
    return schematic

def getPossibleParts(schematic):
    possibleParts = []
    y = 0
    for row in schematic:
        xStart = 0
        xEnd = 0
        x = 0
        inNumber = False
        number = 0
        for c in row:
            if c in digits:
                if not inNumber:
                    inNumber = True
                    xStart = x
                number = number*10 + int(c)
            elif c not in digits:
                if inNumber:
                    xEnd = x - 1
                    possibleParts.append(PossiblePartNumber(schematic, number, xStart, xEnd, y))
                    xStart = 0
                    xEnd = 0
                    number = 0
                    inNumber = False
            x += 1
        y += 1
    return possibleParts

def findNeighboringParts(parts, x, y):
    neighbors = []
    for p in parts:
        if p.isNextTo(x,y):
            neighbors.append(p)
    return neighbors

def findGears(parts, schematic):
    gears = []
    y = 0
    for row in schematic:
        x = 0
        for c in row:
            if c == '*':
                neighbors = findNeighboringParts(parts, x, y)
                if len(neighbors) == 2:
                    gears.append(neighbors[0].number * neighbors[1].number)
                
            x += 1
        y += 1
    return gears

if __name__ == "__main__":
    schematic = buildSchematic(sys.argv[1])
    possibleParts = getPossibleParts(schematic)
    parts = list(filter(lambda x: x.isPartNumber(), possibleParts))
    gears = findGears(parts, schematic)
    print(sum(gears))