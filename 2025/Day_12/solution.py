import sys
import math

def buildGrid(x,y):
    return [['.']*x for i in range(y)]

def cloneGrid(grid):
    return[[x for x in y] for y in grid]

def printGrid(grid):
    for y in grid:
        print("".join(y))

def rotate90(shape):
    # from https://stackoverflow.com/a/53895686
    rotated = [list(reversed(col)) for col in zip(*shape)]
    return rotated

def flipH(shape):
    return [list(reversed(x)) for x in shape]

def flipV(shape):
    return list(reversed(shape))

def equalShapes(s1, s2):
    yLen = len(s1)
    xLen = len(s1[0])
    for y in range(yLen):
        for x in range(xLen):
            if s1[y][x] != s2[y][x]:
                return False
    return True

def removeDuplicates(shapes):
    newShapes=[]
    for s in shapes:
        isNew = True
        for ns in newShapes:
            if equalShapes(s,ns):
                isNew=False
                break;
        if isNew:
            newShapes.append(s)
    return newShapes


def rotateAndFlip(shape):
    """Given a 3x3 grid return all the possible rotations, and
        horizontal and vertical flips of each rotation. With
        any redundant shapes removed.
    """
    variants = [shape]
    variants.append(flipH(shape))
    variants.append(flipV(shape))
    for x in range(3): # rotate 3 times clockwise
        r = rotate90(shape)
        variants.append(r)
        variants.append(flipH(r))
        variants.append(flipV(r))

    return removeDuplicates(variants)


def collision(grid, shape, xOffset, yOffset):
    yLen = len(shape)
    xLen = len(shape[0])
    for y in range(yLen):
        for x in range(xLen):
            if grid[y+yOffset][x+xOffset] == '#' and shape[y][x] == '#':
                return True
    return False
    
def placeShape(grid, shape, xOffset, yOffset):
    printGrid(grid)
    printGrid(shape)
    yLen = len(shape)
    xLen = len(shape[0])
    for y in range(yLen):
        for x in range(xLen):
            c = shape[y][x]
            if c == '#':
                grid[y+yOffset][x+xOffset] = c
    print("*"*32)
    printGrid(grid)

def canPlace(grid, present, x, y):
    if not collision(grid, v, x, y):
        placeShape(grid, v, x, y)
        return True
    return False


def canFit(grid, counts, presents):
    cLen = len(counts)
    total = 0:
    for c in counts:
        total += c
    if total == 0:
        return true;
    for i in range(cLen):
        currentCount = counts[i]
        if currentCount > 0:
            newGrid = cloneGrid(grid)
            for y in range(0, yLen - 2):
                for x in range(0, xLen - 2):
                    for v in present.variants:
                        if canPlace(newGrid, presents[i], x, y):
                            newCounts = [c for c in counts]
                            newCounts[i] -= 1
                            return canFit(newGrid, newCounts, presents)
    return False

class FirGrid:
    def __init__(self, line, presents):
        size, counts = line.split(": ")
        x,y = [int(i) for i in size.split("x")]
        self.x = x
        self.y = y
        self.counts = [int(x) for x in counts.split(" ")]
        self.presents = presents

    def canFit(self):
        grid = buildGrid(self.x, self.y)
        return canFit(grid, self.counts, self.presents)

    def __str__(self):
        return f'{self.x}x{self.y}: {" ".join([str(x) for x in self.counts])}'

class Present:
    def __init__(self, index, shape):
        self.index = index
        self.shape = shape
        self.shape[0] = [x for x in self.shape[0]]
        self.shape[1] = [x for x in self.shape[1]]
        self.shape[2] = [x for x in self.shape[2]]
        self.variants = rotateAndFlip(self.shape)

    def __str__(self):
        s = []
        s.append(f'{self.index}:')
        s.append(f'{"".join(self.shape[0])}')
        s.append(f'{"".join(self.shape[1])}')
        s.append(f'{"".join(self.shape[2])}')
        for v in self.variants:
            s.append("")
            s.append(f'\t{"".join(v[0])}')
            s.append(f'\t{"".join(v[1])}')
            s.append(f'\t{"".join(v[2])}')
        return '\n'.join(s)

def readPresentsAndGrids(filename):
    presents = {}
    grids = []
    lines = []
    with open(filename,'r') as f:
        for l in f.readlines():
            line = l.strip()
            if line:
                lines.append(line)

    index = 0
    while index < len(lines):
        line = lines[index]
        if ':' in line and 'x' not in line: # this is a present
            presentIndex = int(line[:-1])
            shape = [
                lines[index + 1],
                lines[index + 2],
                lines[index + 3],
            ]
            presents[presentIndex] = Present(presentIndex, shape)
            index += 4
        elif 'x' in line and ':' in line: # grid
            grids.append(FirGrid(line, presents))
            index += 1

    return (presents, grids)



if __name__ == "__main__":
    presents, grids = readPresentsAndGrids(sys.argv[1])
    for p in presents:
        print(presents[p])
        print()
    total = 0
    for g in grids:
        print(g)
        grid = buildGrid(g.x, g.y)
        if (g.canFit()):
            total += 1
    print("Total:", total)





