# ..........................
# ..........................
# ..........................
# ..........................
# ..........................
# ..........................
# ..........................
# ..........................
# ..........................
# ..........................
# ..........................
# ..........................
# ..........................
# ..........................
# ..........................
# ...........H..............  (H covers 1, 2, 3, 4, 5, 6, 7, 8, 9, s)
# ..........................
# ..........................
# ..........................
# ..........................
# ..........................

import itertools

def initGrid():
    grid = []
    for x in range(21):
        grid.append(list(itertools.repeat('.', 26)))
    return grid

def drawGrid(hPos, tails, s):
    grid = initGrid() # clear it everytime
    rTails = tails[-1::-1]
    print(hPos)
    print(tails)

    grid[s[1]][s[0]] = 's'

    for i in range(len(rTails)):
        x,y = rTails[i]
        grid[y][x] = str(len(tails)-i)

    grid[hPos[1]][hPos[0]] = 'H'
    for d in grid:
        print(''.join(d))
    print()
    print('*=*=*=*=*=*=*=*=*=*=*=*=*=*=*')
    print()