import sys


def readGrid(filename):
    grid = []
    with open(filename,'r') as f:
        for l in f.readlines():
            line = l.strip()
            grid.append([x for x in line])
    return grid

           
def padGrid(unpaddedGrid):
    """
        given a grid add padding to make the algorithm simpler
    """
    width = len(unpaddedGrid[0]) + 2
    paddedGrid = []
    paddedGrid.append([x for x in "."*width])
    for x in unpaddedGrid:
        paddedGrid.append(["."] + x + ["."])
    paddedGrid.append([x for x in "."*width])
    return paddedGrid

def isAvailable(grid, x, y):
    count = -1 # don't count ourselves
    for i in range(x-1, x+2):
        for j in range(y-1, y+2):
            c = grid[i][j]
            if c == '@':
                count += 1
    return count < 4



def removeAvailableRolls(grid):
    removed = 0
    canRemove = []
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            c = grid[x][y]
            if c == '.':
                continue
            elif (isAvailable(grid, x, y)):
                canRemove.append((x,y))
    removed += len(canRemove)
    if removed > 0:
        for x,y in canRemove:
            grid[x][y]='.'
        return removed + removeAvailableRolls(grid)
    return 0 # none left to remove

def printGrid(grid):
    for x in grid:
        for y in x:
            print(y,end="")
        print()

if __name__ == "__main__":
    total = 0
    grid = padGrid(readGrid(sys.argv[1]))
    printGrid(grid)
    print (removeAvailableRolls(grid))


