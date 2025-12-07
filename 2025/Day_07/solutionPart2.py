import sys
import time

shouldPrint = True
# memoize the splitters so once we have gone down the path we don't go down it again.
# key (x,y) tuple
# value count
splitters = {}

def readGrid(filename):
    grid = []
    with open(filename,'r') as f:
        for l in f.readlines():
            line = l.strip()
            grid.append([x for x in line])
    return grid

           
def printGrid(grid, suffix=""):
    if shouldPrint:
        time.sleep(0.25)
        print(chr(27) + "[0;0f") # move to top of the screen
        for x in grid:
            for y in x:
                print(y,end="")
            print(suffix)

def cloneGrid(oldGrid):
    newGrid = []
    for y in oldGrid:
        newGrid.append([x for x in y])
    return newGrid

def findPaths(grid, currentY, currentCount, depth=1):
    printGrid(grid, " :" + str(currentCount))
    yLen = len(grid)
    xLen = len(grid[0])
    if currentY == yLen: # we made it to the bottom
        return currentCount + 1
    for y in range(currentY, yLen):
        for x in range(xLen):
            current = grid[y][x]
            above = grid[y-1][x]
            if current == '^' and above == '|':
                if (x,y) in splitters:
                    return splitters[(x,y)]
                leftGrid = cloneGrid(grid)
                rightGrid = cloneGrid(grid)
                # go left
                leftGrid[y][x-1] = '|';
                localCount = findPaths(leftGrid, y+1, 0, depth+1)
                # go Right
                rightGrid[y][x+1] = '|';
                localCount += findPaths(rightGrid, y+1, 0, depth+1)
                splitters[(x,y)] = localCount
                return localCount
            elif current == '.':
                if above in ['S','|']:
                    grid[y][x] = '|'
                    printGrid(grid, " :" + str(currentCount))
    return currentCount + 1


if __name__ == "__main__":
    total = 0
    print(chr(27) + "[2J") # clear the screen
    grid = readGrid(sys.argv[1])
    if len(sys.argv) > 2:
        shouldPrint=False
    count = findPaths(grid, 0, 0)
    print(count)


