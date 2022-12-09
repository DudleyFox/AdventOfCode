import itertools

def readGrid():
    grid = []
    with open('input.txt', 'r') as f:
        for l in f.readlines():
            row = [int(x) for x in l.strip()]
            grid.append(row)
    return grid

def computeScoreHelper(t, a):
    count = 0
    for x in a:
        count += 1
        if x >= t:
            return count
    return count
        


def computeScenicScore(x,y, rc, cc, grid):
    t = grid[y][x]
    up = (y == 0 and []) or [grid[i][x] for i in range(y-1, -1, -1)]
    down = (y == rc - 1 and []) or [grid[i][x] for i in range(y+1, rc)]
    left = (x == 0 and []) or [grid[y][i] for i in range(x-1, -1, -1)]
    right = (x == cc - 1 and []) or [grid[y][i] for i in range(x+1, cc)]
    upCount = computeScoreHelper(t, up)
    downCount = computeScoreHelper(t, down)
    leftCount = computeScoreHelper(t, left)
    rightCount = computeScoreHelper(t, right)
    return upCount * downCount * leftCount * rightCount

if __name__ == '__main__':
    grid = readGrid()
    rowCount = len(grid)
    columnCount = len(grid[0])
    score = 0
    for y in range(1, rowCount - 1):
        for x in range(1, columnCount - 1):
            score = max(score, computeScenicScore(y,x, rowCount, columnCount, grid))

    print(score)

        

