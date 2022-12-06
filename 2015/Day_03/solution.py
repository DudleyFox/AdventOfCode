


visited = set()

def getInput():
    with open('input.txt', 'r') as f:
        return f.read().strip()


def nextHouse(current, direction):
    # >^<v
    x,y = current
    if direction == '^':
        y += 1
    elif direction == 'v':
        y -= 1
    elif direction == '>':
        x += 1
    elif direction == '<':
        x -= 1
    return (x,y)

current = (0,0)
visited.add(current)

for x in getInput():
    current = nextHouse(current, x)
    visited.add(current)

print(len(visited))
