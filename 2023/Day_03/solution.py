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


if __name__ == "__main__":
    schematic = buildSchematic(sys.argv[1])
    possibleParts = getPossibleParts(schematic)
    parts = filter(lambda x: x.isPartNumber(), possibleParts)
    print(sum(map(lambda x: x.number, parts)))