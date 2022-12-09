

visited = set()

def readDirections():
    with open('input.txt', 'r') as f:
        return [x for x in f.readlines()]

def moveHead(hPos, c):
    d, i = c.split(' ')
    i = int(i)
    if d == 'U':
        for x in range(1, i+1):
            yield (hPos[0], hPos[1] + x)
    if d == 'D':
        for x in range(1, i+1):
            yield (hPos[0], hPos[1] - x)
    if d == 'L':
        for x in range(1, i+1):
            yield (hPos[0] - x, hPos[1])
    if d == 'R':
        for x in range(1, i+1):
            yield (hPos[0] + x, hPos[1])
    
    return
    
def moveTail(tPos, hPos, visited):
    x1, y1 = hPos
    x2, y2 = tPos
    dx = x1 - x2
    dy = y1 - y2
    mx = 0
    my = 0
    if abs(dx) > 1 and dy == 0:
        mx = dx > 0 and 1 or -1
    if abs(dy) > 1 and dx == 0:
        my = dy > 0 and 1 or -1
    if abs(dx) > 1 and dy != 0:
        mx = dx > 0 and 1 or -1
        my = dy
    if abs(dy) > 1 and dx != 0:
        my = dy > 0 and 1 or -1
        mx = dx
    t = (tPos[0] + mx, tPos[1] + my)
    visited.add(t)
    return t     


def followDirections(directions, visited):
    hPos = (0, 0)
    tPos = (0, 0)
    visited.add(tPos)
    for d in directions:
        for h in moveHead(hPos, d):
            hPos = h
            tPos = moveTail(tPos, hPos, visited)


if __name__ == '__main__':
    directions = readDirections()
    followDirections(directions, visited)
    
    print(visited)
    print(len(visited))
