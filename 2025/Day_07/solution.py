import sys
import time


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

def printGrid(grid):
    time.sleep(0.1)
    print(chr(27) + "[0;0f") # move to top of the screen
    for x in grid:
        for y in x:
            print(y,end="")
        print()

def propagateTachyonBeams(grid):
    splitters = set()
    yLen = len(grid)
    xLen = len(grid[0])
    for y in range(yLen):
        for x in range(xLen):
            current = grid[y][x]
            above = grid[y-1][x]
            if current == '^':
                splitters.add((x,y))
                if above in ['S','|']:
                    grid[y][x+1] = '|'
                    grid[y][x-1] = '|'
            elif current == '.':
                if above in ['S','|']:
                    grid[y][x] = '|'
        printGrid(grid)
    return splitters

def countSplits(grid, splitters):
    count = 0
    for splitter in splitters:
        x,y = splitter
        if grid[y-1][x] in ['S','|']:
            count += 1
    return count


if __name__ == "__main__":
    total = 0
    print(chr(27) + "[2J") # clear the screen
    grid = readGrid(sys.argv[1])
    splitters = propagateTachyonBeams(grid)
    print(countSplits(grid, splitters))


